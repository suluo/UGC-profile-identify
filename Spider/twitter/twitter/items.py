# -*- coding: UTF-8 -*- 
# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class basicItem(Item):
    name = Field()
    name_add = Field()
    declaration = Field()
    link = Field()
    twitter_num = Field()
    following_num = Field()
    followers_num = Field()
    pass

class twitterItem(Item):
    name = Field()
    twitter_name = Field()
    twitter_name_add = Field()
    twitter_content = Field()
    twitter_time = Field()
    pass


class followingItem(Item):
    name = Field()
    following_name = Field()
    following_add = Field()
    following_declaration = Field()
    pass

class followersItem(Item):
    name = Field()
    followers_name = Field()
    following_add = Field()
    followers_declaration = Field()
    pass

class favoritesItem(Item):
    name = Field()
    favorites_name = Field()
    favorites_add = Field()
    favorites_content = Field()
    favorites_time = Field()
    pass

