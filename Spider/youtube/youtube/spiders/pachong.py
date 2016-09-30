# -*- coding: utf-8 -*-
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

from youtube.items import moivepage
from youtube.items import userpage
from youtube.items import usermoive
from youtube.items import userplaymoiveabout
from youtube.items import userplaymoive
from youtube.items import userchanel
from youtube.items import userdiscass
from youtube.items import userintroduvtion
from youtube.items import userfristdiscassmoive
from youtube.items import userseconddiscassmoive

import time
import string
import urllib2
import re
#from BeautifulSoup import BeautifulSoup

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from selenium import selenium
from selenium import webdriver
import time
import twisted

class youtubeSpider(BaseSpider):
    name = "pachong"
    #allow_domains = ["http://www.youtube.com/"]
    #start_urls = ["https://www.youtube.com/channel/UCMsxOweH55dPkGzUOWInY0Q/feed","https://www.youtube.com/watch?v=32wWqHbIHpw"]
    #start_urls = ["https://www.youtube.com/channel/UCqTU7anTSosJ2HZgU5tC-Gw/about"]
    start_urls = ["https://www.youtube.com/channel/UC-lHJZR3Gqxm24_Vd_AJ5Yw/feed","https://www.youtube.com/watch?v=E4aw3y1TAvs"]
        
    def __init__(self):
        BaseSpider.__init__(self)
        self.verificationErrors = []
        # self.profile = webdriver.FirefoxProfile("C:/Users/Administrator/AppData/Roaming/Mozilla/Firefox/Profiles/rbqs2eme")
        # self.browser = webdriver.Firefox(self.profile)
        self.browser = webdriver.Chrome('C:\Users\ZERO\AppData\Local\Google\Chrome\Application\chromedriver.exe')

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
        if response.url not in self.duplicatesurl['url'] :
            self.duplicatesurl['url'].add(response.url)
            if '/watch' in response.url :
                print 1
                return self.watch_parse(response)
            elif '/feed' in response.url:
                print 2
                return self.user_parse(response)
            elif '/videos' in response.url:
                print 3
                return self.videos_parse(response)
            elif '/playlist' in response.url:
                print 4
                if 'list=' in response.url:
                    return self.playlist_parse(response)
                else:
                    return self.playlistabout_parse(response)
            elif ('/channel/' in response.url) and ('/channels' in response.url) :
                print 5
                return self.channels_parse(response)
            elif ('/user' in response.url) and ('/channels' in response.url) :
                print 6
                return self.channels_parse(response)
            elif 'discussion' in response.url:
                print 7
                return self.userdiscass_parse(response)
            elif '/about' in response.url:
                print 8
                return self.userintroduvtion_parse(response)
        else:
            print 9
            pass
        
    def watch_parse(self, response):
                hxs = HtmlXPathSelector(response)
                
                sel = self.browser
                sel.get(response.url)
                time.sleep(10)
                js="var q=document.documentElement.scrollTop=1000000"
                sel.execute_script(js)
                time.sleep(10)
                js="var q=document.documentElement.scrollTop=0"
                sel.execute_script(js)
                time.sleep(10)
                        
                try:
                        #sel.find_element_by_link_text('展开').click()
                        sel.find_element_by_xpath("//button[@class='yt-uix-button yt-uix-button-size-default yt-uix-button-expander yt-uix-expander-head yt-uix-expander-collapsed-body yt-uix-gen204']").click()
                        time.sleep(10)
                except:
                        pass
                        
                hxs = HtmlXPathSelector(text=sel.page_source)
                
                item1 = moivepage()
                if hxs.select('//div[@id="watch-headline-title"]/h1[@class="yt watch-title-container"]/span[@id="eow-title"]/text()').extract():
                        item1['moivename'] = hxs.select('//div[@id="watch-headline-title"]/h1[@class="yt watch-title-container"]/span[@id="eow-title"]/text()').extract()
                else:
                        item1['moivename'] = '0'

                if hxs.select('//div[@class="yt-user-info"]/a/text()').extract():
                        item1['moiveauther'] = hxs.select('//div[@class="yt-user-info"]/a/text()').extract()
                else:
                        item1['moiveauther'] = '0'

                if hxs.select('//span[@id="watch7-subscription-container"]/span[@class=" yt-uix-button-subscription-container"]/span/text()').extract():
                        item1['moivedisnum'] = hxs.select('//span[@id="watch7-subscription-container"]/span[@class=" yt-uix-button-subscription-container"]/span/text()').extract()
                else:
                        item1['moivedisnum'] = '0'

                if hxs.select('//div[@id="watch-description-clip"]/div[@id="watch-uploader-info"]/strong/text()').extract():
                        item1['moivetime'] = hxs.select('//div[@id="watch-description-clip"]/div[@id="watch-uploader-info"]/strong/text()').extract()
                else:
                        item1['moivetime'] = '0'                
   

                if ' '.join(hxs.select('//div[@id="watch-description-clip"]/div[@id="watch-description-text"]/p/text()').extract() + hxs.select('//div[@id="watch-description-clip"]/div[@id="watch-description-text"]/p/a/text()').extract()) :
                        item1['moivecontent'] = ','.join(hxs.select('//div[@id="watch-description-clip"]/div[@id="watch-description-text"]/p/text()').extract() + hxs.select('//div[@id="watch-description-clip"]/div[@id="watch-description-text"]/p/a/text()').extract())
                else :
                        item1['moivecontent'] = '0'

                if hxs.select('//ul[@class="content watch-info-tag-list"]/li/a/text()').extract():
                        item1['moiveclass'] = hxs.select('//ul[@class="content watch-info-tag-list"]/li/a/text()').extract()
                else:
                        item1['moiveclass'] = '0'

                if hxs.select('//div[@id="watch8-sentiment-actions"]/div[@id="watch7-views-info"]/div/text()').extract():
                        item1['watchnum'] = hxs.select('//div[@id="watch8-sentiment-actions"]/div[@id="watch7-views-info"]/div/text()').extract()
                else:
                        item1['watchnum'] = '0'

                if hxs.select('//span[@class="like-button-renderer"]/span[@id="watch-like-dislike-buttons"]/span[1]/button/span/text()').extract():
                        item1['goodnum'] = hxs.select('//span[@class="like-button-renderer"]/span[@id="watch-like-dislike-buttons"]/span[1]/button/span/text()').extract()
                else:
                        item1['goodnum'] = '0'

                if hxs.select('//span[@class="like-button-renderer"]/span[@id="watch-like-dislike-buttons"]/span[3]/button/span/text()').extract():
                        item1['badnum'] = hxs.select('//span[@class="like-button-renderer"]/span[@id="watch-like-dislike-buttons"]/span[3]/button/span/text()').extract()
                else:
                        item1['badnum'] = '0'
                    
                item1['moivepageurl'] = response.url
                yield item1

                for a in range(10):
                        js="var q=document.documentElement.scrollTop=1000000"
                        sel.execute_script(js)
                        time.sleep(5)

                        try:
                                #sel.find_element_by_link_text('展开').click()
                                sel.find_element_by_id("yt-comments-paginator").click()
                                time.sleep(5)
                        except:
                                pass

                        js="var q=document.documentElement.scrollTop=0"
                        sel.execute_script(js)
                        time.sleep(5)

                hxs = HtmlXPathSelector(text=sel.page_source)
                
                item2 = userfristdiscassmoive()
                userfristdiscassmoive_nest= hxs.select('//div[@class="comment-entry"]')
                for postcontent in userfristdiscassmoive_nest:
                        if hxs.select('//div[@id="watch-headline-title"]/h1[@class="yt watch-title-container"]/span[@id="eow-title"]/text()').extract() :
                                item2['moivename'] = hxs.select('//div[@id="watch-headline-title"]/h1[@class="yt watch-title-container"]/span[@id="eow-title"]/text()').extract() 
                        else :
                                item2['moivename'] = '0'                

                        if hxs.select('//div[@class="yt-user-info"]/a/text()').extract():
                                item2['moiveauther'] = hxs.select('//div[@class="yt-user-info"]/a/text()').extract()
                        else :
                                item2['moiveauther'] = '0' 
                

                        if postcontent.select('div[@class="comment-item yt-commentbox-top"]/div[@class="content"]/div[@class="comment-header"]/a/text()').extract() :
                                item2['userfristname'] = postcontent.select('div[@class="comment-item yt-commentbox-top"]/div[@class="content"]/div[@class="comment-header"]/a/text()').extract() 
                        else :
                                item2['userfristname'] = '0'
                                
                        if ' '.join( postcontent.select('div[1]/div[@class="content"]/div[@class="comment-text"]/div/text()').extract() ) :
                                item2['discasscontent'] = ','.join( postcontent.select('div[1]/div[@class="content"]/div[@class="comment-text"]/div/text()').extract() )
                        else :
                                item2['discasscontent'] = '0'

                        if postcontent.select('div[1]/div[@class="content"]/div[@class="comment-header"]/span[@class="time"]/a/text()').extract() :

                                '''timestr = postcontent.select('div[1]/div[@class="content"]/div[@class="comment-header"]/span[@class="time"]/a/text()').extract()
                                timestr = timestr.strip()
                                nowtime = time.strftime('%Y-%m-%d',time.localtime(time.time()))
                                try:
                                        string.atoi(timestr[1], 10)
                                        timenumstr = timestr[:1] 
                                except:
                                        timenumstr = timestr[0]
                                if '天' in timestr :
                                        timenum = string.atoi(timestr, 10)
                                        nowdaynum = string.atoi(nowtime[8:], 10)
                                        if timenum <= nowdaynum :
                                                nowtime = nowtime[:8] + str(nowdaynum-timenum)
                                        else:'''
                                        
                                item2['discasstime'] = ','.join(postcontent.select('div[1]/div[@class="content"]/div[@class="comment-header"]/span[@class="time"]/a/text()').extract()
                                                        + [time.strftime('%Y-%m-%d',time.localtime(time.time()))])
                        else :
                                item2['discasstime'] = '0'

                        item2['userfristdiscassmoiveurl'] = response.url
                        yield item2

                        url_userchannel= postcontent.select('div[@class="comment-item yt-commentbox-top"]/div[@class="content"]/div[@class="comment-header"]/a/@href').extract()
                        for urlsub in url_userchannel: 
                                urlsub1="https://www.youtube.com"+urlsub+"/feed"
                                yield Request(urlsub1,callback = self.parse)
                                urlsub2="https://www.youtube.com"+urlsub+"/videos"
                                yield Request(urlsub2,callback = self.parse)
                                urlsub3="https://www.youtube.com"+urlsub+"/playlists"
                                yield Request(urlsub3,callback = self.parse)
                                urlsub4="https://www.youtube.com"+urlsub+"/channels"
                                yield Request(urlsub4,callback = self.parse)
                                urlsub5="https://www.youtube.com"+urlsub+"/discussion"
                                yield Request(urlsub5,callback = self.parse)
                                urlsub6="https://www.youtube.com"+urlsub+"/about"
                                yield Request(urlsub6,callback = self.parse)


                item3 = userseconddiscassmoive()
                userfristdiscassmoive_nest= hxs.select('//div[@class="comment-entry"]')
                for postcontent in userfristdiscassmoive_nest:
                        userseconddiscassmoive_nest= postcontent.select('div[3]/div[@class="comment-item yt-commentbox-top reply"]')
                        for replaypostcontent in userseconddiscassmoive_nest:                
                                if hxs.select('//div[@id="watch-headline-title"]/h1[@class="yt watch-title-container"]/span[@id="eow-title"]/text()').extract() :
                                        item3['moivename'] = hxs.select('//div[@id="watch-headline-title"]/h1[@class="yt watch-title-container"]/span[@id="eow-title"]/text()').extract() 
                                else :
                                        item3['moivename'] = '0'                          
                        
                                if hxs.select('//div[@class="yt-user-info"]/a/text()').extract():
                                        item3['moiveauther'] = hxs.select('//div[@class="yt-user-info"]/a/text()').extract()
                                else :
                                        item3['moiveauther'] = '0' 

                                if postcontent.select('div[1]/div[@class="content"]/div[@class="comment-header"]/a/text()').extract() :
                                        item3['userfristname'] = postcontent.select('div[1]/div[@class="content"]/div[@class="comment-header"]/a/text()').extract() 
                                else :
                                        item3['userfristname'] = '0'

                                if replaypostcontent.select('div[@class="content"]/div[@class="comment-header"]/a/text()').extract() :
                                        item3['usersecondname'] = replaypostcontent.select('div[@class="content"]/div[@class="comment-header"]/a/text()').extract() 
                                else :
                                        item3['usersecondname'] = '0'

                                if ' '.join(replaypostcontent.select('div[@class="content"]/div[@class="comment-text"]/div/text()').extract()) :
                                        item3['discasscontent'] = ','.join(replaypostcontent.select('div[@class="content"]/div[@class="comment-text"]/div/text()').extract()) 
                                else :
                                        item3['discasscontent'] = '0'

                                if replaypostcontent.select('div[@class="content"]/div[@class="comment-header"]/span[@class="time"]/a/text()').extract() :
                                        item3['discasstime'] = ','.join(replaypostcontent.select('div[@class="content"]/div[@class="comment-header"]/span[@class="time"]/a/text()').extract()
                                                                + [time.strftime('%Y-%m-%d',time.localtime(time.time()))])
                                else :
                                        item3['discasstime'] = '0'

                                item3['userseconddiscassmoiveurl'] = response.url
                                yield item3
                                

    def user_parse(self, response):
                hxs = HtmlXPathSelector(response)

                sel = self.browser
                sel.get(response.url)
                time.sleep(10)

                for a in range(10):
                        js="var q=document.documentElement.scrollTop=1000000"
                        sel.execute_script(js)
                        time.sleep(5)

                        try:
                                #sel.find_element_by_link_text('加载更多').click()
                                sel.find_element_by_xpath("//button[@class='yt-uix-button yt-uix-button-size-default yt-uix-button-default load-more-button yt-uix-load-more browse-items-load-more-button']").click()
                                time.sleep(5)
                        except:
                                pass

                        js="var q=document.documentElement.scrollTop=0"
                        sel.execute_script(js)
                        time.sleep(5)

                hxs = HtmlXPathSelector(text=sel.page_source)
                                
                item4 = userpage()
                userpage_nest= hxs.select('//li[@class="feed-item-container yt-section-hover-container  legacy-style vve-check"]')
                for userpagename in userpage_nest :
                        if hxs.select('//span[@class="qualified-channel-title-wrapper"]/span[@class="qualified-channel-title-text"]/a/text()').extract():
                                item4['username'] = hxs.select('//span[@class="qualified-channel-title-wrapper"]/span[@class="qualified-channel-title-text"]/a/text()').extract()
                        else:
                                item4['username'] = '0'                      

                        if ''.join( userpagename.select('div[@class="feed-item-dismissable post-item "]/div[@class="feed-item-main"]/div[@class="feed-item-main-content"]/div/div/div[@class="yt-lockup-content"]/h3/a/text()').extract() + userpagename.select('div[@class="feed-item-dismissable post-item "]/div[@class="feed-item-main"]/div[@class="feed-item-main-content"]/div/div[@class="yt-lockup-content"]/h3/a/text()').extract() ):
                                item4['channelmoivername'] = ''.join( userpagename.select('div[@class="feed-item-dismissable post-item "]/div[@class="feed-item-main"]/div[@class="feed-item-main-content"]/div/div/div[@class="yt-lockup-content"]/h3/a/text()').extract() + userpagename.select('div[@class="feed-item-dismissable post-item "]/div[@class="feed-item-main"]/div[@class="feed-item-main-content"]/div/div[@class="yt-lockup-content"]/h3/a/text()').extract() )
                        else:
                                item4['channelmoivername'] = '0'

                        if ''.join( userpagename.select('div[@class="feed-item-dismissable post-item "]/div[@class="feed-item-main"]/div/span[@class="feed-item-actions-line"]/text()').extract()):
                                item4['useraction'] = ''.join( userpagename.select('div[@class="feed-item-dismissable post-item "]/div[@class="feed-item-main"]/div/span[@class="feed-item-actions-line"]/text()').extract())
                        else:
                                item4['useraction'] = '0'

                        if ''.join( userpagename.select('div[@class="feed-item-dismissable post-item "]/div[@class="feed-item-main"]/div[@class="feed-item-main-content"]/div/div/div[@class="yt-lockup-content"]/h3/a/@href').extract() + userpagename.select('div[@class="feed-item-dismissable post-item "]/div[@class="feed-item-main"]/div[@class="feed-item-main-content"]/div/div[@class="yt-lockup-content"]/h3/a/@href').extract() ):
                                item4['moiveurl'] = ''.join( userpagename.select('div[@class="feed-item-dismissable post-item "]/div[@class="feed-item-main"]/div[@class="feed-item-main-content"]/div/div/div[@class="yt-lockup-content"]/h3/a/@href').extract() + userpagename.select('div[@class="feed-item-dismissable post-item "]/div[@class="feed-item-main"]/div[@class="feed-item-main-content"]/div/div[@class="yt-lockup-content"]/h3/a/@href').extract() )
                        else:
                                item4['moiveurl'] = '0'

                        if ''.join(userpagename.select('div[@class="feed-item-dismissable post-item "]/div[@class="feed-item-main"]/div[@class="feed-item-main-content"]/div/div/div[@class="yt-lockup-content"]/div[@class="yt-lockup-meta"]/ul/li/text()').extract()
                                   + userpagename.select('div[@class="feed-item-dismissable post-item "]/div[@class="feed-item-main"]/div[@class="feed-item-main-content"]/div/div[@class="yt-lockup-content"]/div[@class="yt-lockup-meta"]/ul/li/text()').extract()
                                   + userpagename.select('div[@class="feed-item-dismissable post-item "]/div[@class="feed-item-main"]/div[@class="feed-item-main-content"]/div/div[@class="yt-lockup-content"]/div[@class="yt-lockup-badges"]/span/span/text()').extract() ):
                                item4['channelmoivecontent'] = ','.join(userpagename.select('div[@class="feed-item-dismissable post-item "]/div[@class="feed-item-main"]/div[@class="feed-item-main-content"]/div/div/div[@class="yt-lockup-content"]/div[@class="yt-lockup-meta"]/ul/li/text()').extract()
                                   + userpagename.select('div[@class="feed-item-dismissable post-item "]/div[@class="feed-item-main"]/div[@class="feed-item-main-content"]/div/div[@class="yt-lockup-content"]/div[@class="yt-lockup-meta"]/ul/li/text()').extract()
                                   + userpagename.select('div[@class="feed-item-dismissable post-item "]/div[@class="feed-item-main"]/div[@class="feed-item-main-content"]/div/div[@class="yt-lockup-content"]/div[@class="yt-lockup-badges"]/span/span/text()').extract() )
                        else:
                                item4['channelmoivecontent'] = '0'

                        if userpagename.select('div[@class="feed-item-dismissable post-item "]/div[@class="feed-item-main"]/div/span[@class="feed-item-actions-line"]/span[@class="feed-item-time"]/text()').extract():
                                item4['channelmoivetime'] = ','.join(userpagename.select('div[@class="feed-item-dismissable post-item "]/div[@class="feed-item-main"]/div/span[@class="feed-item-actions-line"]/span[@class="feed-item-time"]/text()').extract()
                                                        + [time.strftime('%Y-%m-%d',time.localtime(time.time()))])
                        else:
                                item4['channelmoivetime'] = '0'

                        item4['userpageurl'] = response.url
                        yield item4


    def videos_parse(self, response):
                hxs = HtmlXPathSelector(response)

                sel = self.browser
                sel.get(response.url)
                time.sleep(5)

                for a in range(10):
                        js="var q=document.documentElement.scrollTop=1000000"
                        sel.execute_script(js)
                        time.sleep(5)

                        try:
                                #sel.find_element_by_link_text('加载更多').click()
                                sel.find_element_by_xpath("//button[@class='yt-uix-button yt-uix-button-size-default yt-uix-button-default load-more-button yt-uix-load-more browse-items-load-more-button']").click()
                                time.sleep(5)
                        except:
                                pass

                        js="var q=document.documentElement.scrollTop=0"
                        sel.execute_script(js)
                        time.sleep(5)

                hxs = HtmlXPathSelector(text=sel.page_source)
                                
                item5 = usermoive()
                usermoive_nest= hxs.select('//li[@class="channels-content-item yt-shelf-grid-item"]')
                for usermoivename in usermoive_nest :
                        if hxs.select('//span[@class="qualified-channel-title-wrapper"]/span[@class="qualified-channel-title-text"]/a/text()').extract():
                                item5['username'] = hxs.select('//span[@class="qualified-channel-title-wrapper"]/span[@class="qualified-channel-title-text"]/a/text()').extract()
                        else:
                                item5['username'] = '0' 

                        if usermoivename.select('div[@class="yt-lockup clearfix  yt-lockup-video yt-lockup-grid vve-check"]/div[@class="yt-lockup-dismissable"]/div[@class="yt-lockup-content"]/h3/a/text()').extract():
                                item5['moivename'] = usermoivename.select('div[@class="yt-lockup clearfix  yt-lockup-video yt-lockup-grid vve-check"]/div[@class="yt-lockup-dismissable"]/div[@class="yt-lockup-content"]/h3/a/text()').extract()
                        else:
                                item5['moivename'] = '0'

                        if usermoivename.select('div[@class="yt-lockup clearfix  yt-lockup-video yt-lockup-grid vve-check"]/div[@class="yt-lockup-dismissable"]/div[@class="yt-lockup-content"]/div[@class="yt-lockup-byline"]/a/text()').extract():
                                item5['moiveauther'] = usermoivename.select('div[@class="yt-lockup clearfix  yt-lockup-video yt-lockup-grid vve-check"]/div[@class="yt-lockup-dismissable"]/div[@class="yt-lockup-content"]/div[@class="yt-lockup-byline"]/a/text()').extract()
                        else:
                                item5['moiveauther'] = '0'

                        if usermoivename.select('div[@class="yt-lockup clearfix  yt-lockup-video yt-lockup-grid vve-check"]/div[@class="yt-lockup-dismissable"]/div[@class="yt-lockup-content"]/h3/a/@href').extract():
                                item5['moiveurl'] = usermoivename.select('div[@class="yt-lockup clearfix  yt-lockup-video yt-lockup-grid vve-check"]/div[@class="yt-lockup-dismissable"]/div[@class="yt-lockup-content"]/h3/a/@href').extract()
                        else:
                                item5['moiveurl'] = '0'

                        if ''.join(usermoivename.select('div[@class="yt-lockup clearfix  yt-lockup-video yt-lockup-grid vve-check"]/div[@class="yt-lockup-dismissable"]/div[@class="yt-lockup-content"]/div[@class="yt-lockup-meta"]/ul/li/text()').extract()):
                                item5['timewatchnum'] = ','.join( usermoivename.select('div[@class="yt-lockup clearfix  yt-lockup-video yt-lockup-grid vve-check"]/div[@class="yt-lockup-dismissable"]/div[@class="yt-lockup-content"]/div[@class="yt-lockup-meta"]/ul/li/text()').extract())
                        else:
                                item5['timewatchnum'] = '0'

                        item5['usermoiveurl'] = response.url
                        yield item5

                        url_usermoive = usermoivename.select('div[@class="yt-lockup clearfix  yt-lockup-video yt-lockup-grid vve-check"]/div[@class="yt-lockup-dismissable"]/div[@class="yt-lockup-content"]/h3/a/@href').extract()
                        for urlsub in url_usermoive: 
                                urlsub1="https://www.youtube.com"+urlsub
                                yield Request(urlsub1,callback = self.parse,priority = 60)


    def playlistabout_parse(self, response):
                hxs = HtmlXPathSelector(response)
                
                sel = self.browser
                sel.get(response.url)
                time.sleep(10)
                hxs = HtmlXPathSelector(text=sel.page_source)


                item6 = userplaymoiveabout()
                playlistabout_nest= hxs.select('//li[@class="channels-content-item yt-shelf-grid-item"]')
                for playlistaboutname in playlistabout_nest :
                        if hxs.select('//span[@class="qualified-channel-title-wrapper"]/span[@class="qualified-channel-title-text"]/a/text()').extract():
                                item6['username'] = hxs.select('//span[@class="qualified-channel-title-wrapper"]/span[@class="qualified-channel-title-text"]/a/text()').extract()
                        else:
                                item6['username'] = '0' 

                        if playlistaboutname.select('div[@class="yt-lockup clearfix  yt-lockup-playlist yt-lockup-grid"]/div[@class="yt-lockup-dismissable"]/div[@class="yt-lockup-content"]/h3/a/text()').extract():
                                item6['playmoivetype'] = playlistaboutname.select('div[@class="yt-lockup clearfix  yt-lockup-playlist yt-lockup-grid"]/div[@class="yt-lockup-dismissable"]/div[@class="yt-lockup-content"]/h3/a/text()').extract()
                        else:
                                item6['playmoivetype'] = '0'

                        if playlistaboutname.select('div[@class="yt-lockup clearfix  yt-lockup-playlist yt-lockup-grid"]/div[@class="yt-lockup-dismissable"]/div[@class="yt-lockup-content"]/h3/a/@href').extract():
                                item6['playmoivetypeurl'] = playlistaboutname.select('div[@class="yt-lockup clearfix  yt-lockup-playlist yt-lockup-grid"]/div[@class="yt-lockup-dismissable"]/div[@class="yt-lockup-content"]/h3/a/@href').extract()
                        else:
                                item6['playmoivetypeurl'] = '0'
                       
                        item6['userplaymoiveabouturl'] = response.url
                        yield item6

                        url_playlistabout = playlistaboutname.select('div[@class="yt-lockup clearfix  yt-lockup-playlist yt-lockup-grid"]/div[@class="yt-lockup-dismissable"]/div[@class="yt-lockup-content"]/h3/a/@href').extract()
                        for urlsub in url_playlistabout: 
                                urlsub1="https://www.youtube.com"+urlsub
                                yield Request(urlsub1,callback = self.parse,priority = 100)


    def playlist_parse(self, response):
                hxs = HtmlXPathSelector(response)

                sel = self.browser
                sel.get(response.url)
                time.sleep(5)

                for a in range(10):
                        js="var q=document.documentElement.scrollTop=1000000"
                        sel.execute_script(js)
                        time.sleep(5)

                        try:
                                #sel.find_element_by_link_text('加载更多').click()
                                sel.find_element_by_xpath("//button[@class='yt-uix-button yt-uix-button-size-default yt-uix-button-default load-more-button yt-uix-load-more browse-items-load-more-button']").click()
                                time.sleep(5)
                        except:
                                pass

                        js="var q=document.documentElement.scrollTop=0"
                        sel.execute_script(js)
                        time.sleep(5)

                hxs = HtmlXPathSelector(text=sel.page_source)
                                
                item7 = userplaymoive()
                userplaymoive_nest= hxs.select('//tr[@class="pl-video yt-uix-tile "]')
                for userplaymoivename in userplaymoive_nest :
                        if hxs.select('//span[@class="qualified-channel-title-wrapper"]/span[@class="qualified-channel-title-text"]/a/text()').extract():
                                item7['username'] = hxs.select('//span[@class="qualified-channel-title-wrapper"]/span[@class="qualified-channel-title-text"]/a/text()').extract()
                        else:
                                item7['username'] = '0' 

                        if hxs.select('//div[@class="branded-page-box clearfix"]/div[@class="pl-header-content "]/h1/text()').extract():
                                item7['playmoivetype'] = hxs.select('//div[@class="branded-page-box clearfix"]/div[@class="pl-header-content "]/h1/text()').extract()
                        else:
                                item7['playmoivetype'] = '0'

                        if ''.join( hxs.select('//div[@class="branded-page-box clearfix"]/div[@class="pl-header-content "]/ul/li/text()').extract() ):
                                item7['userplaymoivecontent'] = ','.join( hxs.select('//div[@class="branded-page-box clearfix"]/div[@class="pl-header-content "]/ul/li/text()').extract() )
                        else:
                                item7['userplaymoivecontent'] = '0'

                        if userplaymoivename.select('td[@class="pl-video-title"]/a/text()').extract():
                                item7['moivename'] = userplaymoivename.select('td[@class="pl-video-title"]/a/text()').extract()
                        else:
                                item7['moivename'] = '0'
                                
                        if userplaymoivename.select('td[@class="pl-video-title"]/div[@class="pl-video-owner"]/a/text()').extract():
                                item7['moiveauther'] = userplaymoivename.select('td[@class="pl-video-title"]/div[@class="pl-video-owner"]/a/text()').extract()
                        else:
                                item7['moiveauther'] = '0'

                        if userplaymoivename.select('td[@class="pl-video-title"]/a/@href').extract():
                                item7['moiveurl'] = userplaymoivename.select('td[@class="pl-video-title"]/a/@href').extract()
                        else:
                                item7['moiveurl'] = '0'

                        if userplaymoivename.select('td[@class="pl-video-time"]/div[@class="more-menu-wrapper"]/div[@class="timestamp"]/span/text()').extract():
                                item7['watchmoivetime'] = ','.join(userplaymoivename.select('td[@class="pl-video-time"]/div[@class="more-menu-wrapper"]/div[@class="timestamp"]/span/text()').extract()
                                                        + [time.strftime('%Y-%m-%d',time.localtime(time.time()))])
                        else:
                                item7['watchmoivetime'] = '0'

                        item7['userplaymoiveurl'] = response.url
                        yield item7



    def channels_parse(self, response):
                hxs = HtmlXPathSelector(response)

                sel = self.browser
                sel.get(response.url)
                time.sleep(5)

                for a in range(10):
                        js="var q=document.documentElement.scrollTop=1000000"
                        sel.execute_script(js)
                        time.sleep(5)

                        try:
                                #sel.find_element_by_link_text('加载更多').click()
                                sel.find_element_by_xpath("//button[@class='yt-uix-button yt-uix-button-size-default yt-uix-button-default load-more-button yt-uix-load-more browse-items-load-more-button']").click()
                                time.sleep(5)
                        except:
                                pass

                        js="var q=document.documentElement.scrollTop=0"
                        sel.execute_script(js)
                        time.sleep(5)

                hxs = HtmlXPathSelector(text=sel.page_source)
                                
                item8 = userchanel()
                userchanel_nest= hxs.select('//li[@class="channels-content-item yt-shelf-grid-item"]')
                for userchanelname in userchanel_nest :
                        if hxs.select('//span[@class="qualified-channel-title-wrapper"]/span[@class="qualified-channel-title-text"]/a/text()').extract():
                                item8['username'] = hxs.select('//span[@class="qualified-channel-title-wrapper"]/span[@class="qualified-channel-title-text"]/a/text()').extract()
                        else:
                                item8['username'] = '0' 

                        if userchanelname.select('div[@class="yt-lockup clearfix  yt-lockup-channel yt-lockup-grid"]/div[@class="yt-lockup-content"]/h3/a/text()').extract():
                                item8['chanelname'] = userchanelname.select('div[@class="yt-lockup clearfix  yt-lockup-channel yt-lockup-grid"]/div[@class="yt-lockup-content"]/h3/a/text()').extract()
                        else:
                                item8['chanelname'] = '0'

                        if userchanelname.select('div[@class="yt-lockup clearfix  yt-lockup-channel yt-lockup-grid"]/div[@class="yt-lockup-content"]/h3/a/@href').extract():
                                item8['chanelurl'] = userchanelname.select('div[@class="yt-lockup clearfix  yt-lockup-channel yt-lockup-grid"]/div[@class="yt-lockup-content"]/h3/a/@href').extract()
                        else:
                                item8['chanelurl'] = '0'

                        if userchanelname.select('div[@class="yt-lockup clearfix  yt-lockup-channel yt-lockup-grid"]/div[@class="yt-lockup-content"]/span/span/text()').extract():
                                item8['discribenum'] = userchanelname.select('div[@class="yt-lockup clearfix  yt-lockup-channel yt-lockup-grid"]/div[@class="yt-lockup-content"]/span/span/text()').extract()
                        else:
                                item8['discribenum'] = '0'

                        item8['userchanelurl'] = response.url
                        yield item8


    def userdiscass_parse(self, response):
                print 10
                hxs = HtmlXPathSelector(response)                

                sel = self.browser
                sel.get(response.url)
                time.sleep(10)
                hxs = HtmlXPathSelector(text=sel.page_source)
                
                item9 = userdiscass()
                print 11
                userdiscass_nest= hxs.select('//div[@class="VW Bn"]/div[@class="pga"]/div')
                print 12
                print len(userdiscass_nest)
                for userdiscassname in userdiscass_nest :
                        print 13
                        if hxs.select('//span[@class="qualified-channel-title-wrapper"]/span[@class="qualified-channel-title-text"]/a/text()').extract():
                                item9['username'] = hxs.select('//span[@class="qualified-channel-title-wrapper"]/span[@class="qualified-channel-title-text"]/a/text()').extract()
                        else:
                                item9['username'] = '0' 

                        if userdiscassname.select('div[@class="ju"]/div[@class="ki"]/div[@class="ve oba HPa"]/div[@class="f5 wy"]/header[@class="lea"]/h3/a/span/text()').extract():
                                item9['userdiscassname'] = userdiscassname.select('div[@class="ju"]/div[@class="ki"]/div[@class="ve oba HPa"]/div[@class="f5 wy"]/header[@class="lea"]/h3/a/span/text()').extract()
                        else:
                                item9['userdiscassname'] = '0'

                        if userdiscassname.select('div[@class="ju"]/div[@class="ki"]/div[@class="ve oba HPa"]/div[@class="pf Al"]/div[@class="Xx xJ"]/div/div/div[@class="Ct"]/text()').extract():
                                item9['discasscontent'] = userdiscassname.select('div[@class="ju"]/div[@class="ki"]/div[@class="ve oba HPa"]/div[@class="pf Al"]/div[@class="Xx xJ"]/div/div/div[@class="Ct"]/text()').extract()
                        else:
                                item9['discasscontent'] = '0'

                        if userdiscassname.select('div[@class="ju"]/div[@class="ki"]/div[@class="ve oba HPa"]/div[@class="f5 wy"]/header[@class="lea"]/span/span/a/text()').extract():
                                item9['discasstime'] = ','.join(userdiscassname.select('div[@class="ju"]/div[@class="ki"]/div[@class="ve oba HPa"]/div[@class="f5 wy"]/header[@class="lea"]/span/span/a/text()').extract()
                                                + [time.strftime('%Y-%m-%d',time.localtime(time.time()))])
                        else:
                                item9['discasstime'] = '0'

                        item9['userdiscassurl'] = response.url
                        yield item9

    def userintroduvtion_parse(self, response):
                hxs = HtmlXPathSelector(response)
                
                sel = self.browser
                sel.get(response.url)
                time.sleep(10)
                hxs = HtmlXPathSelector(text=sel.page_source)

                item10 = userintroduvtion()
                if hxs.select('//span[@class="qualified-channel-title-wrapper"]/span[@class="qualified-channel-title-text"]/a/text()').extract():
                        item10['username'] = hxs.select('//span[@class="qualified-channel-title-wrapper"]/span[@class="qualified-channel-title-text"]/a/text()').extract()
                else:
                        item10['username'] = '0'

                if ''.join( hxs.select('//div[@class="about-metadata-container"]/div[@class="about-description branded-page-box-padding"]/p/text()').extract() ):
                        item10['userintroduvtion'] = ' '.join( hxs.select('//div[@class="about-metadata-container"]/div[@class="about-description branded-page-box-padding"]/p/text()').extract() )
                else:
                        item10['userintroduvtion'] = '0'

                if ''.join( hxs.select('//li[@class="channel-links-item"]/a/@href').extract() ):
                        item10['otherlinkurl'] = ','.join( hxs.select('//li[@class="channel-links-item"]/a/@href').extract() )
                else:
                        item10['otherlinkurl'] = '0'

                item10['userintroduvtionurl'] = response.url
                yield item10
