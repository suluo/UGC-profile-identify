# -*- coding: UTF-8 -*- 
# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from scrapy.http import TextResponse

from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals

from facebook.items import fb_postItem
from facebook.items import fb_Item

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from selenium import selenium
from selenium import webdriver
import time
import twisted

class facebookSpider(BaseSpider):
    name = "pachong"
    #allow_domains = ["https://plus.google.com/"]
    start_urls = ["https://www.facebook.com/theamandablain"]
                
    def __init__(self):
        BaseSpider.__init__(self)
        self.verificationErrors = []
        self.profile = webdriver.FirefoxProfile("C:/Users/Administrator/AppData/Roaming/Mozilla/Firefox/Profiles/rbqs2eme.")
        self.browser = webdriver.Firefox(self.profile)
                
        self.duplicatesurl = {}
        dispatcher.connect(self.spider_opened, signals.spider_opened)
        dispatcher.connect(self.spider_closed, signals.spider_closed)
                
    def __del__(self):
        print self.verificationErrors
        #pass
        
    def spider_opened(self, spider):
        self.duplicatesurl['url'] = set()

    def spider_closed(self, spider):
        del self.duplicatesurl['url']

    def parse(self, response):
        if '/about' in response.url:
            return self.about_parse(response)
        else:
            return self.post_parse(response)

    def post_parse(self, response):
        hxs = HtmlXPathSelector(response)
        sel = self.browser
        sel.get(response.url)
        time.sleep(20)

        for a in range(2):
            js="var q=document.documentElement.scrollTop=1000000"
            sel.execute_script(js)
            time.sleep(5)

            try:
                sel.find_element_by_link_text('显示较早的动态').click()
                time.sleep(15)
            except Exception as e:
                pass

            js="var q=document.documentElement.scrollTop=0"
            sel.execute_script(js)
            time.sleep(3)

            hxs = HtmlXPathSelector(text=sel.page_source)
                
            item1 = fb_postItem()
            fb_name_nest= hxs.select('//div[@role="article"]')
            for name in fb_name_nest :
                if name.select('div[@class="clearfix mbs pbs _1_m"]/div[@class="_3dp _29k"]/h5/span/span/a/text()').extract():
                    item1['username'] = name.select('div[@class="clearfix mbs pbs _1_m"]/div[@class="_3dp _29k"]/h5/span/span/a/text()').extract()
                else :
                    item1['username'] = '0'

                if ' '.join(name.select('div[@class="aboveUnitContent"]/div[@class="userContentWrapper"]/div[@class="_wk"]/span/span/text()').extract() + name.select('div[@class="aboveUnitContent"]/div[@class="userContentWrapper"]/div[@class="_wk"]/span/text()').extract() + name.select('div[@class="userContentWrapper"]/div[@class="_wk mbm"]/span/div/text()').extract() + name.select('div[@class="_1x1"]/div[@class="userContentWrapper"]/div[@class="_wk"]/span/text()').extract()) :
                    item1['post'] = ' '.join(name.select('div[@class="aboveUnitContent"]/div[@class="userContentWrapper"]/div[@class="_wk"]/span/span/text()').extract() + name.select('div[@class="aboveUnitContent"]/div[@class="userContentWrapper"]/div[@class="_wk"]/span/text()').extract() + name.select('div[@class="userContentWrapper"]/div[@class="_wk mbm"]/span/div/text()').extract() + name.select('div[@class="_1x1"]/div[@class="userContentWrapper"]/div[@class="_wk"]/span/text()').extract())
                else :
                    item1['post'] = '0'

                if name.select('div[@class="clearfix mbs pbs _1_m"]/div[@class="_3dp _29k"]/div[@class="_1_n fsm fwn fcg"]/a/abbr/@title').extract():
                    item1['time'] = name.select('div[@class="clearfix mbs pbs _1_m"]/div[@class="_3dp _29k"]/div[@class="_1_n fsm fwn fcg"]/a/abbr/@title').extract()
                else :
                    item1['time'] = '0'

                yield item1

    def about_parse(self, response):
        hxs = HtmlXPathSelector(response)

        sel = self.browser
        sel.get(response.url)
        time.sleep(20)

        try:
            sel.find_element_by_link_text('查看全部').click()
            time.sleep(10)
        except:
             pass

        hxs = HtmlXPathSelector(text=sel.page_source)

        item2 = fb_Item()
        if hxs.select('//div[@class="_6-e"]/h2[@class="_6-f"]/a/text()').extract() :
            item2['username'] = hxs.select('//div[@class="_6-e"]/h2[@class="_6-f"]/a/text()').extract()
        else:
            item2['username'] = '0'

        if ' '.join(hxs.select('//div[@class="experienceContent"]/div[@class="experienceTitle"]/a/text()').extract() + hxs.select('//div[@class="experienceContent"]/div[@class="experienceBody fsm fwn fcg"]/span/text()').extract()) :
            item2['WorkExp'] = ','.join(hxs.select('//div[@class="experienceContent"]/div[@class="experienceTitle"]/a/text()').extract() + hxs.select('//div[@class="experienceContent"]/div[@class="experienceBody fsm fwn fcg"]/span/text()').extract())
        else:
            item2['WorkExp'] = '0'

        if ' '.join(hxs.select('//div[@id="pagelet_basic"]/div/table/tbody/tr/td/div/div/text()').extract() + hxs.select('//div[@id="pagelet_basic"]/div/table/tbody/tr/th/text()').extract()) :
            item2['Basic'] = ' '.join(hxs.select('//div[@id="pagelet_basic"]/div/table/tbody/tr/td/div/div/text()').extract() + hxs.select('//div[@id="pagelet_basic"]/div/table/tbody/tr/th/text()').extract())
        else:
            item2['Basic'] = '0'

        if hxs.select('//div[@class="_6a _6b"]/div[@class="fsl fwb fcb"]/a/text()').extract() :
            item2['page'] = hxs.select('//div[@class="_6a _6b"]/div[@class="fsl fwb fcb"]/a/text()').extract()
        else:
            item2['page'] = '0'

        if ' '.join(hxs.select('//div[@id="pagelet_contact"]/div/div/table/tbody/tr/td/ul/li/a/@href').extract() ):
            item2['contact'] = ' '.join(hxs.select('//div[@id="pagelet_contact"]/div/div/table/tbody/tr/td/ul/li/a/@href').extract())
        else:
            item2['contact'] = '0'

        if ' '.join(hxs.select('//div[@id="pagelet_bio"]/div/div[2]/text()').extract() + hxs.select('//div[@id="pagelet_bio"]/div/div[2]/a/text()').extract()) :
            item2['about'] = ' '.join(hxs.select('//div[@id="pagelet_bio"]/div/div[2]/text()').extract() + hxs.select('//div[@id="pagelet_bio"]/div/div[2]/a/text()').extract())
        else:
            item2['about'] = '0'

        if ' '.join(hxs.select('//div[@id="pagelet_quotes"]/div/div[2]/text()').extract()) :
            item2['favorite'] = ' '.join(hxs.select('//div[@id="pagelet_quotes"]/div/div[2]/text()').extract())
        else:
            item2['favorite'] = '0'

        if ' '.join(hxs.select('//div[@id="current_city"]/div[@class="_42ef"]/div[@class="_6a"]/div[@class="_6a _6b"]/div[@class="fsl fwb fcb"]/a/text()').extract() + hxs.select('//div[@id="current_city"]/div[@class="_42ef"]/div[@class="_6a"]/div[@class="_6a _6b"]/div[@class="aboutSubtitle fsm fwn fcg"]/text()').extract()) :
            item2['location'] = ' '.join(hxs.select('//div[@id="current_city"]/div[@class="_42ef"]/div[@class="_6a"]/div[@class="_6a _6b"]/div[@class="fsl fwb fcb"]/a/text()').extract() + hxs.select('//div[@id="current_city"]/div[@class="_42ef"]/div[@class="_6a"]/div[@class="_6a _6b"]/div[@class="aboutSubtitle fsm fwn fcg"]/text()').extract())
        else:
            item2['location'] = '0'

        yield item2
