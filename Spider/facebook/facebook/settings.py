# Scrapy settings for facebook project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'facebook'

SPIDER_MODULES = ['facebook.spiders']
NEWSPIDER_MODULE = 'facebook.spiders'

DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
    'facebook.middlewares.ProxyMiddleware': 100,
}

DOWNLOAD_DELAY = 5

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'facebook (+http://www.yourdomain.com)'
