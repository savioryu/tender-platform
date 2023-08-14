import scrapy

class SzggzySpider(scrapy.Spider):
    name = 'szggzy'
    allowed_domains = ['szggzy.com']
    start_urls = ['https://www.szggzy.com/jygg/list.html']

    def parse(self, response):
        # 获取所有采购公告的链接
        # links = response.css('#list_zfcg li .li-a::attr(href)').getall()
        # print('~~~~~~~~~~~links', links)
        a_tags = response.css('#list_zfcg').getall()
        print('~~~~~~~~~~~a_tags', a_tags)
        # hrefs = a_tags.xpath('@href').getall()
        # print('~~~~~~~~~~~hrefs', hrefs)
        # for link in links:
        #     yield response.follow(link, callback=self.parse_notice)

        # # 获取下一页链接并继续爬取
        # next_page = response.css('.ewb-page-next a::attr(href)').get()
        # if next_page:
        #     yield response.follow(next_page, callback=self.parse)

    def parse_notice(self, response):
        # 获取项目名称
        title = response.css('.ewb-article h1::text').get()

        # 获取预算金额
        budget = response.css('.ewb-article p:contains("预算金额")::text').get()

        # 获取开标时间
        open_time = response.css('.ewb-article p:contains("开标时间")::text').get()

        # 获取采购人信息
        purchaser = response.css('.ewb-article p:contains("采购人")::text').get()

        # 获取采购代理机构信息
        agent = response.css('.ewb-article p:contains("采购代理机构")::text').get()

        # 获取公告附件文件链接
        attachment = response.css('.ewb-article a[href$=".docx"]::attr(href)').get()

        # 输出结果
        yield {
            'title': title,
            'budget': budget,
            'open_time': open_time,
            'purchaser': purchaser,
            'agent': agent,
            'attachment': attachment
        }