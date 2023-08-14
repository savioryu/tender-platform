from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

# 导入你的 Spider 类
from szggzy_interface import SzggzySpider

# 导入随机 User-Agent 中间件
from scrapy_fake_useragent.middleware import RandomUserAgentMiddleware

# 创建 Scrapy 设置对象
settings = Settings()

# 设置你的自定义 User-Agent（可选）
# settings.set('USER_AGENT', 'your_custom_user_agent')

# 添加随机 User-Agent 中间件到中间件列表
settings.set('DOWNLOADER_MIDDLEWARES', {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
})

settings.set('LOG_LEVEL', 'DEBUG')
             
# 创建 CrawlerProcess 并使用自定义设置
process = CrawlerProcess(settings)

# 启动 Spider
process.crawl(SzggzySpider)
process.start()
