# Scrapy settings for youtube project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'youtube'

SPIDER_MODULES = ['youtube.spiders']
NEWSPIDER_MODULE = 'youtube.spiders'

DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
    'youtube.middlewares.ProxyMiddleware': 100,
}

ITEM_PIPELINES = ['youtube.pipelines.youtubePipeline']
DEPTH_LIMIT = 10000
DOWNLOAD_DELAY = 5

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'youtube (+http://www.yourdomain.com)'
