# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field

class JpmovieItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = Field()
    cover = Field()
    directors = Field()
    writers = Field()
    actors = Field()
    types = Field()
    released = Field()
    mins = Field()
    alias = Field()
    imdb = Field()
    intro = Field()
    #download images
    image_urls = Field()
    images = Field()

