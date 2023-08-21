import scrapy
import json
import re
import requests
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from datetime import datetime, timedelta
from fake_useragent import UserAgent

# 创建 UserAgent 对象
user_agent = UserAgent()
proxypool_url = 'http://127.0.0.1:5555/random'

class SzggzySpider(scrapy.Spider):
    name = 'szggzy'
    allowed_domains = ['szggzy.com']
    start_urls = ['https://www.szggzy.com/cms/api/v1/trade/content/page']
    #部署时注意修改
    mongo_uri = 'mongodb://127.0.0.1:27017/'
    mongo_database = 'tender_purchase'
    mongo_user = 'tender'
    mongo_password = 'tender12345'
    collection_name = 'tender_purchase_list'

    def __init__(self, *args, **kwargs):
        super(SzggzySpider, self).__init__(*args, **kwargs)
        startDate = kwargs.get('startDate')
        endDate = kwargs.get('endDate')
        # 只要未输入 startDate，连同 endDate 都设置为当天
        if startDate is None:
            today = datetime.today().strftime('%Y-%m-%d')
            startDate = today
            endDate = today
        # 未输入 endDate，endDate 设置为 startDate
        if endDate is None:
            endDate = startDate
        # 将输入日期字符串转换为 datetime 对象
        self.startDate = datetime.strptime(startDate, '%Y-%m-%d')
        self.endDate = datetime.strptime(endDate, '%Y-%m-%d')
        print(f"Date Range: {self.startDate} ~ {self.endDate}")

    def convert_time(self, date):
        # 生成查询时间段
        release_time_begin = date.strftime('%Y-%m-%d 00:00:00')
        release_time_end = (date + timedelta(days=1) - timedelta(seconds=1)).strftime('%Y-%m-%d 23:59:59')
        return release_time_begin, release_time_end

    def start_requests(self):
        currentDate = self.startDate
        while currentDate <= self.endDate:
            [release_time_begin, release_time_end] = self.convert_time(currentDate)
            for url in self.start_urls:
                data = {
                    'modelId':1378,
                    'channelId':2850,
                    'fields':[
                        {'fieldName':'jygg_gglxmc_rank1','fieldValue':'采购公告'}, 
                    ],
                    'title': None,
                    'releaseTimeBegin': release_time_begin,
                    'releaseTimeEnd': release_time_end,
                    'page': 0,
                    'size': 100
                }
                # 源列表接口对于 2022-08-04 后的数据才能使用 jygg_gglxmc 过滤
                if (currentDate > datetime(2022, 8, 4)):
                    data['fields'].append({'fieldName': 'jygg_gglxmc', 'fieldValue': '采购公告'})

                headers = {
                    'Content-Type': 'application/json',
                    'Referer': 'https://www.szggzy.com/jygg/list.html'
                }
                # print('======================================================================')
                # print(data)
                body = json.dumps(data)
                yield scrapy.FormRequest(url, method='POST', headers=headers, body=body, callback=self.parse_all, meta={'currentDate': currentDate})
                currentDate += timedelta(days=1)
    
    # 处理公告列表接口返回的数据
    def parse_all(self, response):
        # 处理响应
        rsp = json.loads(response.text)
        url_list = self.parse_url_list(rsp['data']['content'])
        currentDate = response.meta['currentDate']
        currentDateStr = currentDate.strftime('%Y-%m-%d')
        totalElements = rsp['data']['totalElements']
        # 记录当次爬取总数
        self.crawler.stats.set_value(f"zero-{currentDateStr}", totalElements)
        if(totalElements >= 100):
            self.record_retry_date({'date': currentDateStr, 'totalElements': totalElements})

        # Debug
        # mockData = [
        #     { 
        #         'contentId': '1808539',
        #     },
        # ]
        # url_list = self.parse_url_list(mockData)

        # 构造新的请求，继续爬取另外的接口
        for url_item in url_list:
            user_agent_random = user_agent.random
            # print(f"User-Agent: {user_agent_random}")
            # 处理接口防爬
            headers = {
                'Referer': url_item['web_url'],
                'User-Agent': user_agent_random
            }
            yield scrapy.Request(url=url_item['api_url'], headers=headers, callback=self.parse_detail, errback=self.handle_detail_error, meta={'url_item': url_item})
        pass
    
    # 单条数据请求异常处理
    def handle_detail_error(self, failure):
        request = failure.request
        exception_type = failure.type
        error_message = failure.getErrorMessage()

        print(f"Request failed url: {request.url}")
        print(f"Request failed meta: {request.meta}")
        print(f"Exception type: {exception_type}")
        print(f"Exception message: {error_message}")
        pass
    
    # 预处理列表数据
    def parse_url_list(self, data):
        # 对数据进行处理，返回处理后的结果
        url_list = []
        for item in data:
            contentId = str(item['contentId'])
            url_item = {
                'contentId': contentId,
                'api_url': 'https://www.szggzy.com/cms/api/v1/trade/content/detail?contentId=' + contentId,
                'web_url': 'https://www.szggzy.com/jygg/details.html?contentId=' + contentId
            }
            url_list.append(url_item)
        return url_list
    
    # 解析单条数据
    def parse_detail(self, response):
        print('========================================================================================================================')
        print('【web_url】: ', response.meta['url_item']['web_url'])
        rawInfo = self.get_raw_info(response)
        self.parse_process_aggregate(rawInfo)
        print('========================================================================================================================')
        return

    # 获取接口中的原始数据
    def get_raw_info(self, response):
        contentId = response.meta['url_item']['contentId']
        rsp = json.loads(response.text)
        title = rsp['data']['title']
        releaseTime = rsp['data']['releaseTime']
        updateTime = rsp['data']['updateTime']
        attrs = rsp['data']['attrs']
        attachments = next((item for item in attrs if item['attrName'] == 'jygg_fjzy'), None)
        txt = rsp['data']['txt']
        return {
            'contentId': contentId,
            'title': title,
            'releaseTime': releaseTime,
            'updateTime': updateTime,
            'attachments': attachments,
            'txt': txt
        }
    
    # 模板解析聚合
    def parse_process_aggregate(self, rawInfo):
        txt = rawInfo['txt']
        # 处理换行符
        txt = re.sub(r'\n', '<br>', txt)
        txt = re.sub(r'(\t|&nbsp;|\u3000|\u2002)', '', txt)

        pattern_table = re.compile(r'^[\s\S]*<table width="100%".*?</table>')
        pattern_common = re.compile(r'^[\s\S]*<p.*</p>')
        
        result = None
        if pattern_table.match(txt) != None:
            result = self.parse_template_table(txt)
        elif pattern_common.match(txt) != None:
            result = self.parse_template_common(txt)
        else:
            print('【ERROR】: 未知的模板类型')
            pass
        if(result != None):
            # 将数据导入MongoDB
            rawInfo.update(result)
            # del rawInfo['txt']
            self.save_to_mongodb(rawInfo)

    # 获取公告的基础信息
    def get_base_info(self, selector, tag):
        project_name = selector.xpath(fr'string(//{tag}[re:test(., "(项目名称)", "i")])').re_first(r"项目名称[\s\S]*[:|：]\s*(.*)")
        budget = selector.xpath(fr'string(//{tag}[re:test(., "(预算金额|预估金额|支付上限|预算上限|项目金额)", "i")])').re_first(r"[预算金额|预估金额|支付上限|预算上限|项目金额][\s\S]*[:|：]\s*(.*)")
        bid_opening_time = selector.xpath(fr'string(//{tag}[re:test(., "(定于.*?开标|\.开标时间|及开标时间|\.谈判时间|投标响应开始时间)", "i")])').re_first(r"(\d{4}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日\s*\d{1,2}\s*(?:[：:时|点]\s*\d{1,2}\s*分?){0,2}(?:\s*\d{1,2}\s*秒?)?(?:（北京时间）)?)")
        # 兼容开标时间会换行的情况
        if (bid_opening_time == None):
            bid_opening_time = self.get_info(selector, tag, fr"(定于.*?开标|\.开标时间|及开标时间|\.谈判时间|投标响应开始时间)", r"(\d{4}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日\s*\d{1,2}\s*(?:[：:时|点]\s*\d{1,2}\s*分?){0,2}(?:\s*\d{1,2}\s*秒?)?(?:（北京时间）)?)")
        return {
            'project_name': project_name,
            'budget': budget,
            'bid_opening_time': bid_opening_time,
        }

    # 通用获取信息方法
    def get_info(self, selector, tag, title, field):
        # 使用 re() 方法调用 re 模块中的函数
        pattern = fr"{field}.*[:|：]\s*(.*)"
        elements = selector.xpath(fr'//{tag}[re:test(., "{title}", "i")]/following-sibling::{tag}[re:test(., "{pattern}", "i")]')

        # print('--------------------------------------------')
        # print(selector.xpath(fr'//{tag}[re:test(., "{title}", "i")]').get())
        # 返回匹配的结果
        return elements.xpath('string(.)').re_first(pattern)

    # 获取采购人信息
    def get_purchaser_info(self, selector, tag):
        purchaser_title = fr'[.|．|、|）]\s*采购人信息'
        purchaser_name = self.get_info(selector, tag, purchaser_title, '名[\s\S\u3000]*称')
        purchaser_address = self.get_info(selector, tag, purchaser_title, '地[\s\S\u3000]*址')
        purchaser_phone = self.get_info(selector, tag, purchaser_title, '(?:联系方式|电话)')

        return {
            'purchaser_name': purchaser_name,
            'purchaser_address': purchaser_address,
            'purchaser_phone': purchaser_phone,
        }

    # 获取采购代理机构信息
    def get_agency_info(self, selector, tag):
        agency_title = fr'[2|二][.|.|．|、|）]\s*(采购实施机构信息|采购代理机构|采购机构|招标机构|政府集中采购机构|招标代理机构|采购代理机构信息)'
        agency_name = self.get_info(selector, tag, agency_title, '名[\s\S\u3000]*称')
        agency_address = self.get_info(selector, tag, agency_title, '地[\s\S\u3000]*址')
        agency_phone = self.get_info(selector, tag, agency_title, '(?:联系方式|电话)')

        return {
            'agency_name': agency_name,
            'agency_address': agency_address,
            'agency_phone': agency_phone,
        }
    
    # 解析通用模板
    def parse_template_common(self, txt):
        match_tag = '*[self::p or self::h3]'
        selector = scrapy.Selector(text=txt)
        # 获取各类信息
        base_info = self.get_base_info(selector, match_tag)
        purchaser_info = self.get_purchaser_info(selector, match_tag)
        agency_info = self.get_agency_info(selector, match_tag)

        info = {}
        for d in [base_info, purchaser_info, agency_info]:
            info.update(d)
        print('【common tempate】info:\n', info)
        return info

    # 解析表格类模板
    def parse_template_table(self, txt):
        match_tag = 'span'
        selector = scrapy.Selector(text=txt).xpath('//table/tbody/tr/td')
        # 获取各类信息
        base_info = self.get_base_info(selector, match_tag)
        purchaser_info = self.get_purchaser_info(selector, match_tag)
        agency_info = self.get_agency_info(selector, match_tag)

        info = {}
        for d in [base_info, purchaser_info, agency_info]:
            info.update(d)
        print('【table template】info:\n', info)
        return info
    
    # 保存数据到 MongoDB
    def save_to_mongodb(self, data):
        # print(self.mongo_uri, self.mongo_user, self.mongo_password, self.mongo_database, self.collection_name)

        # 连接MongoDB
        # client = MongoClient(self.mongo_uri, username=self.mongo_user, password=self.mongo_password)
        client = MongoClient(self.mongo_uri)
        db = client[self.mongo_database]
        collection = db[self.collection_name]
        
        try:
            # 使用 contentId 字段来查询是否存在记录
            existing_record = collection.find_one({'contentId': data['contentId']})
            if existing_record:
                # 如果记录存在，执行更新操作
                collection.update_one({'contentId': data['contentId']}, {'$set': data})
                print(f"【MongoDB】Record updated 【{data['contentId']}】")
            else:
                # 如果记录不存在，执行插入操作
                collection.insert_one(data)
                print(f"【MongoDB】Record inserted 【{data['contentId']}】")
        except DuplicateKeyError as e:
            # 处理 DuplicateKeyError 异常
            print("捕获到重复键错误：", e)
            print("错误代码:", e.code)
    
    def record_retry_date(self, obj):
        client = MongoClient(self.mongo_uri)
        db = client[self.mongo_database]
        collection = db['retry_date']
        collection.insert_one(obj)