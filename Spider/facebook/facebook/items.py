# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class fb_postItem(Item):
    username = Field()
    post = Field()
    time = Field()
    pass

class fb_Item(Item):
    username = Field()
    WorkExp = Field()
    Basic = Field()
    page = Field()
    contact = Field()
    about = Field()
    favorite = Field()
    location = Field()
    pass

