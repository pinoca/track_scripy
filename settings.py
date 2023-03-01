# Scrapy settings for track_spiders project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "track_spiders"

SPIDER_MODULES = ["track_spiders.spiders"]
NEWSPIDER_MODULE = "track_spiders.spiders"


# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'DpdUK (+http://www.yourdomain.com)'
# 是否遵循爬虫协议
# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# 下载器总共最大处理的并发请求数，默认值16
# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 40
# 爬虫请求超时秒数
DOWNLOAD_TIMEOUT = 2
# 超时重试次数
MAX_RETRY_TIMES = 1
# # Configure a delay for requests for the same website (default: 0)
# # See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# # See also autothrottle settings and docs
# 如果没有开启智能限速，这个值就代表一个规定死的值，代表对同一网址延迟请求的秒数
DOWNLOAD_DELAY = 0
# The download delay setting will honor only one of:

# 每个域名能够被执行的最大并发请求数目，默认值8
CONCURRENT_REQUESTS_PER_DOMAIN = 100
# 能够被单个IP处理的并发请求数，默认值0，代表无限制，如果不为零，将影响CONCURRENT_REQUESTS_PER_DOMAIN和DOWNLOAD_DELAY的限制情况
CONCURRENT_REQUESTS_PER_IP = 100

# 是否支持cookie，cookiejar进行操作cookie，默认开启
# Disable cookies.txt (enabled by default)
COOKIES_ENABLED = True

# Disable Telnet Console (enabled by default)
# 指定是否启用telnet控制台
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# Scrapy发送HTTP请求默认使用的请求头
# DEFAULT_REQUEST_HEADERS ={
#
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# 包含项目中启用的spider中间件及其命令的字典
# SPIDER_MIDDLEWARES = {
#    'Web17TRACK.middlewares.Web17TrackSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# Scrapy中默认启用的下载程序中间件的字典。低值更接近引擎，高值更接近下载器
DOWNLOADER_MIDDLEWARES = {
    "scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware": None,
    "scrapy.downloadermiddlewares.useragent.UserAgentMiddleware": None,
    # 'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
    # 'track_spiders.middlewares.My_RetryMiddleware': 700,
    "track_spiders.middlewares.TrackSpidersDownloaderMiddleware": 543,
    "track_spiders.middlewares.ProxyMiddleware": 200,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# 包含项目中启用的扩展及其顺序的字典
# EXTENSIONS = {

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# 连接的数据库名称
MONGODB_DB = "mws"
MONGODB_COLLECT = "tracker"
MONGODB_HOST = "127.0.0.1"
MONGODB_PORT = 27017
# 包含要使用的项目管道及其顺序的字典。值是任意的，但是习惯上将它们定义在0-1000范围内。低值优先于高值
ITEM_PIPELINES = {
    "track_spiders.pipelines.TrackSpidersPipeline": 300,
}
# 智能限速/自动节流
# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# #开启智能限速/自动节流，默认False不开启
# AUTOTHROTTLE_ENABLED = True
# #The initial download delay
# #起始的延迟
# AUTOTHROTTLE_START_DELAY = 2
# #最大延迟
# #The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# #The average number of requests Scrapy should be sending in parallel to
# #each remote server
# #每秒并发请求数的平均值，不能高于CONCURRENT_REQUESTS_PER_DOMAIN或CONCURRENT_REQUESTS_PER_IP，
# #实际并发请求数目可能高于或低于该值，视爬虫情况而定
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# #Enable showing throttling stats for every response received:
# #调试
# AUTOTHROTTLE_DEBUG = False
LOG_LEVEL = "INFO"  # 输出级别
LOG_STDOUT = True  # 是否标准输出
# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# 是否启用缓存策略
# 缓存超时时间
# 缓存保存路径
# 缓存忽略的HTTP状态码
# 缓存存储的插件
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
