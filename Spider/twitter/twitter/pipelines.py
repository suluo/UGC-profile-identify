# -*- coding: utf-8 -*-
import sys
import MySQLdb
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from scrapy.exceptions import DropItem
import string
reload(sys)
sys.setdefaultencoding('utf8')
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy import create_engine
from sqlalchemy.orm import mapper, sessionmaker
from datetime import datetime
from sqlalchemy import Table, MetaData, Column, ForeignKey, Integer, String, Unicode, DateTime


class TwitterPipeline(object):
    def __init__(self):
        self.duplicates = {}
        dispatcher.connect(self.spider_opened, signals.spider_opened)
        dispatcher.connect(self.spider_closed, signals.spider_closed)
	
    def spider_opened(self, spider):
        self.duplicates['basicItem'] = set()
        self.duplicates['twitterItem1'] = set()
        self.duplicates['twitterItem2'] = set()

    def spider_closed(self, spider):
        del self.duplicates['basicItem']
        del self.duplicates['twitterItem1']
        del self.duplicates['twitterItem2']
	
    def process_item(self, item, spider):
        mysql_engine = create_engine("mysql://root:1234@localhost:3306/twitterbest?charset=utf8&use_unicode=0",echo=True)#创建到数据库的连接,echo=True 表示用logging输出调试结果
        metadata = MetaData(mysql_engine) #跟踪表属性

        if item.has_key('name_add'):
            if item['name'][0] in self.duplicates['basicItem']:
                raise DropItem("Duplicate item found: %s" % item)
            else:
                self.duplicates['basicItem'].add(item['name'][0])
    
            user_table = Table('basicItem', metadata, autoload=True, autoload_with=mysql_engine)	
            stmt = user_table.insert()
            stmt.execute(name=item['name'][0], name_add=item['name_add'][0], declaration=item['declaration'], link=item['link'][0], twitter_num=item['twitter_num'][0], following_num=item['following_num'][0], followers_num=item['followers_num'][0])

        elif item.has_key('twitter_name'):
            '''
            if item['name'][0] in self.duplicates['twitterItem1'] and item['twitter_content'] in self.duplicates['twitterItem2'] :
                raise DropItem("Duplicate item found: %s" % item)
            else:
                self.duplicates['twitterItem1'].add(item['name'][0])
                self.duplicates['twitterItem2'].add(item['twitter_content'])
            '''
            user_table = Table('twitterItem', metadata, autoload=True, autoload_with=mysql_engine)	
            stmt = user_table.insert()
            stmt.execute(name=item['name'][0], twitter_name=item['twitter_name'][0], twitter_name_add=item['twitter_name_add'][0], twitter_content=item['twitter_content'], twitter_time=item['twitter_time'][0])
           
        return item




