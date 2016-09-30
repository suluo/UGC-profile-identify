# -*- coding: UTF-8 -*- 
# Scrapy settings for twitterbest project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'twitter'

SPIDER_MODULES = ['twitter.spiders']
NEWSPIDER_MODULE = 'twitter.spiders'

DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
    'twitter.middlewares.ProxyMiddleware': 100,
}

ITEM_PIPELINES = ['twitter.pipelines.TwitterPipeline']
#COOKIES_ENABLED = False
DOWNLOAD_DELAY = 5

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'twitter (+http://www.yourdomain.com)'
