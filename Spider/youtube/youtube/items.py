# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class moivepage(Item):     # 1
    moivename = Field()
    moiveauther = Field()
    moivedisnum = Field()
    moivetime = Field()
    moivecontent = Field()
    moiveclass = Field()
    watchnum = Field()
    goodnum = Field()
    badnum = Field()
    moivepageurl = Field()
    pass

class userpage(Item):    # 2
    username = Field()
    channelmoivername = Field()
    useraction = Field()
    moiveurl = Field()
    channelmoivecontent = Field()
    channelmoivetime = Field()
    userpageurl = Field()
    pass

class usermoive(Item):   # 3
    username = Field()
    moivename = Field()
    moiveauther = Field()
    moiveurl = Field()
    timewatchnum = Field()
    usermoiveurl = Field()
    pass

class userplaymoiveabout(Item):  # 4
    username = Field()
    playmoivetype = Field()
    playmoivetypeurl = Field()
    userplaymoiveabouturl = Field()
    pass


class userplaymoive(Item):   # 5
    username = Field()
    playmoivetype = Field()
    userplaymoivecontent = Field()
    moivename = Field()
    moiveauther = Field()
    moiveurl = Field()
    watchmoivetime = Field()
    userplaymoiveurl = Field()
    pass

class userchanel(Item):  # 6
    username = Field()
    chanelname = Field()
    chanelurl = Field()
    discribenum = Field()
    userchanelurl = Field()
    pass

class userdiscass(Item):     # 7
    username = Field()
    userdiscassname = Field()  
    discasscontent = Field()
    discasstime = Field()
    userdiscassurl = Field()
    pass

class userintroduvtion(Item):    # 8
    username = Field()
    userintroduvtion = Field()
    otherlinkurl = Field()
    userintroduvtionurl = Field()
    pass

class userfristdiscassmoive(Item):   # 9
    moivename = Field()
    moiveauther = Field()
    userfristname = Field()  
    discasscontent = Field()
    discasstime = Field()
    userfristdiscassmoiveurl = Field()
    pass


class userseconddiscassmoive(Item):  # 10
    moivename = Field()
    moiveauther = Field()
    userfristname = Field()
    usersecondname = Field()
    discasscontent = Field()
    discasstime = Field()
    userseconddiscassmoiveurl = Field()
    pass














