# -*- coding: utf-8 -*-
import sys
import MySQLdb
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from scrapy.exceptions import DropItem
import string
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy.exceptions import DropItem
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy import create_engine
from sqlalchemy.orm import mapper, sessionmaker
from datetime import datetime
from sqlalchemy import Table, MetaData, Column, ForeignKey, Integer, String, Unicode, DateTime

reload(sys)
sys.setdefaultencoding('utf8')

class youtubePipeline(object):
    def __init__(self):
        self.duplicates = {}
        dispatcher.connect(self.spider_opened, signals.spider_opened)
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_opened(self, spider):
        self.duplicates['moivepage'] = set()
        self.duplicates['usermoive'] = set()
        self.duplicates['userplaymoiveabout'] = set()

    def spider_closed(self, spider):
        del self.duplicates['moivepage']
        del self.duplicates['usermoive']
        del self.duplicates['userplaymoiveabout']
	
    def process_item(self, item, spider):
        mysql_engine = create_engine("mysql://root:1234@localhost:3306/youtube?charset=utf8&use_unicode=0",echo=True)
        #创建到数据库的连接,echo=True 表示用logging输出调试结果
        metadata = MetaData(mysql_engine) #跟踪表属性

        if item.has_key('goodnum'):  # 1
            user_table = Table('moivepage', metadata, autoload=True, autoload_with=mysql_engine)	
            stmt = user_table.insert()
            stmt.execute(moivename=item['moivename'][0], moiveauther=item['moiveauther'][0], moivedisnum=item['moivedisnum'][0], moivetime=item['moivetime'][0],
                         moivecontent=item['moivecontent'], moiveclass=item['moiveclass'][0], watchnum=item['watchnum'][0], goodnum=item['goodnum'][0],
                         badnum=item['badnum'][0], moivepageurl=item['moivepageurl'])

        elif item.has_key('channelmoivetime'):  # 2
            user_table = Table('userpage', metadata, autoload=True, autoload_with=mysql_engine)	
            stmt = user_table.insert()
            stmt.execute(username=item['username'][0], channelmoivername=item['channelmoivername'], useraction=item['useraction'], moiveurl=item['moiveurl'],
                         channelmoivecontent=item['channelmoivecontent'], channelmoivetime=item['channelmoivetime'], userpageurl=item['userpageurl'])

        elif item.has_key('timewatchnum'):  # 3
            user_table = Table('usermoive', metadata, autoload=True, autoload_with=mysql_engine)	
            stmt = user_table.insert()
            stmt.execute(username=item['username'][0], moivename=item['moivename'][0], moiveauther=item['moiveauther'][0], moiveurl=item['moiveurl'][0],
                         timewatchnum=item['timewatchnum'], usermoiveurl=item['usermoiveurl'])

        elif item.has_key('playmoivetypeurl'):  # 4
            user_table = Table('userplaymoiveabout', metadata, autoload=True, autoload_with=mysql_engine)	
            stmt = user_table.insert()
            stmt.execute(username=item['username'][0], playmoivetype=item['playmoivetype'][0], playmoivetypeurl=item['playmoivetypeurl'][0],
                         userplaymoiveabouturl=item['userplaymoiveabouturl'])

        elif item.has_key('watchmoivetime'):  # 5
            user_table = Table('userplaymoive', metadata, autoload=True, autoload_with=mysql_engine)	
            stmt = user_table.insert()
            stmt.execute(username=item['username'][0], playmoivetype=item['playmoivetype'][0], userplaymoivecontent=item['userplaymoivecontent'], moivename=item['moivename'][0],
                         moiveauther=item['moiveauther'][0], moiveurl=item['moiveurl'][0], watchmoivetime=item['watchmoivetime'], userplaymoiveurl=item['userplaymoiveurl'])

        elif item.has_key('discribenum'):  # 6
            user_table = Table('userchanel', metadata, autoload=True, autoload_with=mysql_engine)	
            stmt = user_table.insert()
            stmt.execute(username=item['username'][0], chanelname=item['chanelname'][0], chanelurl=item['chanelurl'][0], discribenum=item['discribenum'][0],
                         userchanelurl=item['userchanelurl'])

        elif item.has_key('userdiscassurl'):  # 7
            user_table = Table('userdiscass', metadata, autoload=True, autoload_with=mysql_engine)	
            stmt = user_table.insert()
            stmt.execute(username=item['username'][0], userdiscassname=item['userdiscassname'][0], discasscontent=item['discasscontent'][0], discasstime=item['discasstime'],
                         userdiscassurl=item['userdiscassurl'])

        elif item.has_key('otherlinkurl'):  # 8
            user_table = Table('userintroduvtion', metadata, autoload=True, autoload_with=mysql_engine)	
            stmt = user_table.insert()
            stmt.execute(username=item['username'][0], userintroduvtion=item['userintroduvtion'], otherlinkurl=item['otherlinkurl'], userintroduvtionurl=item['userintroduvtionurl'])

        elif item.has_key('userfristdiscassmoiveurl'):  # 9
            user_table = Table('userfristdiscassmoive', metadata, autoload=True, autoload_with=mysql_engine)	
            stmt = user_table.insert()
            stmt.execute(moivename=item['moivename'][0], moiveauther=item['moiveauther'][0],userfristname=item['userfristname'][0], discasscontent=item['discasscontent'],
                         discasstime=item['discasstime'], userfristdiscassmoiveurl=item['userfristdiscassmoiveurl'])

        elif item.has_key('userseconddiscassmoiveurl'):  # 10
            user_table = Table('userseconddiscassmoive', metadata, autoload=True, autoload_with=mysql_engine)	
            stmt = user_table.insert()
            stmt.execute(moivename=item['moivename'][0], moiveauther=item['moiveauther'][0],userfristname=item['userfristname'][0],usersecondname=item['usersecondname'][0], discasscontent=item['discasscontent'],
                         discasstime=item['discasstime'], userseconddiscassmoiveurl=item['userseconddiscassmoiveurl'])
        return item








        
