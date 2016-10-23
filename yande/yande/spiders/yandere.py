# -*- coding: utf-8 -*-
from scrapy import Request, Spider
from scrapy.selector import Selector
from yande.items import YandeItem


class YandereSpider(Spider):
    name = "yandere"
    allowed_domains = ["yande.re"]
    start_urls = ['https://yande.re/post?page=%d' %x for x in range(1, 7322)]
    base_url = 'https://yande.re'


    def parse(self, response):
    	item = YandeItem()
    	se = Selector(response)
    	thumbs = se.xpath('//*[@class="thumb"]/img/@src').extract()
    	detail_url = se.xpath('//*[@class="thumb"]/@href').extract()
    	for index, url in enumerate(detail_url):
    		yield Request(self.base_url + url, callback=self.parse_detail, meta={'thumb': thumbs[index]})

    def parse_detail(self, response):
    	item = YandeItem()
    	se = Selector(response)
    	item['title'] = se.xpath('//*[@id="image"]/@alt').extract()[0]
    	item['image_urls'] = se.xpath('//*[@id="image"]/@src').extract()
    	item['thumb'] = response.meta['thumb']
    	yield item
        
