# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class HentaiItem(Item):
    # define the fields for your item here like:
    title = Field()
    price = Field()
    pubtime = Field()
    publisher = Field()
    code = Field()
    summary = Field()
    cover = Field()
    staff = Field()
    pics = Field()
    origin = Field()


