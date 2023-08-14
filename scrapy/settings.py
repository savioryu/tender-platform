LOG_LEVEL = 'DEBUG'
LOG_FORMAT = '%(asctime)s [%(name)s] %(levelname)s: %(message)s [User-Agent: %(request_user_agent)s]'

ITEM_PIPELINES = {
    'scrapy-tender.pipelines.MongoDBPipeline': 300,
}
DOWNLOADER_MIDDLEWARES = {
    # ...
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
    # ...
}
