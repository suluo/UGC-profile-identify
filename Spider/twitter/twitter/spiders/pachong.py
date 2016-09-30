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

from twitterbest.items import basicItem
from twitterbest.items import twitterItem
from twitterbest.items import followingItem
from twitterbest.items import followersItem
from twitterbest.items import favoritesItem


from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from selenium import selenium
from selenium import webdriver
import time
import twisted


class twitterSpider(BaseSpider):
    name = "pachong"
    allow_domains = ["http://twitter.com"]
    start_urls = ["https://twitter.com/NBCTheVoice"]

    def __init__(self):
                BaseSpider.__init__(self)
                self.verificationErrors = []
                self.profile = webdriver.FirefoxProfile("C:/Users/Administrator/AppData/Roaming/Mozilla/Firefox/Profiles/rbqs2eme.liuyajun")
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
                
                hxs = HtmlXPathSelector(response)

                item1 = basicItem()
                item1['name'] = hxs.select('//div[@class="profile-card-inner"]/h1[@class="fullname editable-group"]/span/text()').extract()
                item1['name_add'] = hxs.select('//h2[@class="username"]/span[@class="screen-name"]/text()').extract()
                #item1['declaration'] = hxs.select('//div[@class="bio-container editable-group"]/p[@class="bio profile-field"]/text()').extract()
                #item1.setdefault('declaration',[]).append(' '.join(hxs.select('//div[@class="bio-container editable-group"]/p[@class="bio profile-field"]/text()').extract() + hxs.select('//div[@class="bio-container editable-group"]/p/a/s/text()').extract() + hxs.select('//div[@class="bio-container editable-group"]/p/a/b/text()').extract()))
                item1['declaration'] = ' '.join(hxs.select('//div[@class="bio-container editable-group"]/p[@class="bio profile-field"]/text()').extract() + hxs.select('//div[@class="bio-container editable-group"]/p/a/s/text()').extract() + hxs.select('//div[@class="bio-container editable-group"]/p/a/b/text()').extract())

                if hxs.select('//span[@class="url editable-group"]/span[@class="profile-field"]/a/@title').extract() :
                     item1['link'] = hxs.select('//span[@class="url editable-group"]/span[@class="profile-field"]/a/@title').extract()
                else:
                    item1['link'] = 0
                item1['twitter_num'] = hxs.select('//a[@data-element-term="tweet_stats"]/strong/text()').extract()
                item1['following_num'] = hxs.select('//a[@data-element-term="following_stats"]/strong/text()').extract()
                item1['followers_num'] = hxs.select('//a[@data-element-term="follower_stats"]/strong/text()').extract()
                yield item1  


                if response.url not in self.duplicatesurl['url'] :
                        self.duplicatesurl['url'].add(response.url)

                
                        sel = self.browser
                        sel.get(response.url)
                        time.sleep(10)

                        for a in range(70):
                                js="var q=document.documentElement.scrollTop=1000000"
                                sel.execute_script(js)
                                time.sleep(3)
                
                        hxs = HtmlXPathSelector(text=sel.page_source)


                        item2 = twitterItem()
                        name_nest= hxs.select('//div[@class="content"]')
                        for name in name_nest :
                                item2['name'] = hxs.select('//div[@class="profile-card-inner"]/h1[@class="fullname editable-group"]/span/text()').extract()
                
                                if name.select('div[@class="stream-item-header"]/a/strong/text()').extract() :
                                        item2['twitter_name'] = name.select('div[@class="stream-item-header"]/a/strong/text()').extract()
                                else :
                                        item2['twitter_name'] = '0'

                                if name.select('div[@class="stream-item-header"]/a/span/b/text()').extract() :
                                        item2['twitter_name_add'] = name.select('div[@class="stream-item-header"]/a/span/b/text()').extract()
                                else :
                                        item2['twitter_name_add'] = '0'
                
                                if ' '.join(name.select('p/text()').extract() + name.select('p/a/s/text()').extract() + name.select('p/a/b/text()').extract()) :
                                        item2['twitter_content'] = ' '.join(name.select('p/text()').extract() + name.select('p/a/s/text()').extract() + name.select('p/a/b/text()').extract())
                                else :
                                        item2['twitter_content'] = '0'

                                if name.select('div[@class="stream-item-header"]/small[@class="time"]/a/@title').extract() :
                                        item2['twitter_time'] = name.select('div[@class="stream-item-header"]/small[@class="time"]/a/@title').extract()
                                else :
                                        item2['twitter_time'] = '0'
                        
                                yield item2
               
                        
                
                        furl = hxs.select('//div[@class="content"]/div[@class="stream-item-header"]/a/@href').extract()
                        furl = list(set(furl))
                        for furlsub in furl:
                                furlsub="https://twitter.com"+furlsub
                                yield Request(furlsub,callback = self.parse)

                else:
                        pass
                

                '''item1 = basicItem()
                item1['name'] = hxs.select('//div[@class="profile-card-inner"]/h1[@class="fullname editable-group"]/span/text()').extract()
                item1['name_add'] = hxs.select('//h2[@class="username"]/span[@class="screen-name"]/text()').extract()
                #item1['declaration'] = hxs.select('//div[@class="bio-container editable-group"]/p[@class="bio profile-field"]/text()').extract()
                #item1.setdefault('declaration',[]).append(' '.join(hxs.select('//div[@class="bio-container editable-group"]/p[@class="bio profile-field"]/text()').extract() + hxs.select('//div[@class="bio-container editable-group"]/p/a/s/text()').extract() + hxs.select('//div[@class="bio-container editable-group"]/p/a/b/text()').extract()))
                item1['declaration'] = ' '.join(hxs.select('//div[@class="bio-container editable-group"]/p[@class="bio profile-field"]/text()').extract() + hxs.select('//div[@class="bio-container editable-group"]/p/a/s/text()').extract() + hxs.select('//div[@class="bio-container editable-group"]/p/a/b/text()').extract())
            
                item1['link'] = hxs.select('//span[@class="url editable-group"]/span[@class="profile-field"]/a/@title').extract()
                item1['twitter_num'] = hxs.select('//ul[@class="stats js-mini-profile-stats"]/li[1]/a/strong/text()').extract()
                item1['following_num'] = hxs.select('//a[@data-element-term="following_stats"]/strong/text()').extract()
                item1['followers_num'] = hxs.select('//a[@data-element-term="follower_stats"]/strong/text()').extract()
                yield item1  '''


 
                '''for name in sel.find_element_by_xpath('//div[@class="content"]') :

                        nameweb = sel.find_element_by_xpath('//div[@class="profile-card-inner"]/h1[@class="fullname editable-group"]/span')
                        item2['name'] = nameweb.text
                                  
                        
                        twitter_nameweb = name.find_element_by_xpath('div[@class="stream-item-header"]/a/strong')
                        if twitter_nameweb:
                                item2['twitter_name'] = twitter_nameweb.text
                        else :
                                item2['twitter_name'] = '0'
                                
                        twitter_name_addweb = name.find_element_by_xpath('div[@class="stream-item-header"]/a/span/b')
                        if twitter_name_addweb :
                                item2['twitter_name_add'] = twitter_name_addweb.text
                        else :
                                item2['twitter_name_add'] = '0'

                        twitter_contentweb1 = name.find_element_by_xpath('p')
                        twitter_contentweb2 = name.find_element_by_xpath('p/a/s')
                        twitter_contentweb3 = name.find_element_by_xpath('p/a/b')
                        if twitter_contentweb1 or twitter_contentweb2 or twitter_contentweb3:
                                item2['twitter_content'] = ' '.join(twitter_contentweb1.text + twitter_contentweb2.text + twitter_contentweb3.text)
                        else :
                                item2['twitter_content'] = '0'
                                
                        twitter_timeweb = name.find_element_by_xpath('div[@class="stream-item-header"]/small[@class="time"]/a')
                        if twitter_timeweb :
                                item2['twitter_time'] = twitter_timeweb.get_attribute("title")   
                        else :
                                item2['twitter_time'] = '0'
                        
                        yield item2  '''              
                
            
            
            








