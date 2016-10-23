# -*- coding: utf-8 -*-
from scrapy.http.request import Request
from scrapy.selector import Selector
from crawler.items import HentaiItem
from scrapy import Spider

class HentaiSpider(Spider):
	name = 'hentai'
	allowed_domains = ['www.getchu.com']
	start_urls = ['http://www.getchu.com/anime/adult_list.html?page=%d' %x for x in range(1, 11)]

	def start_requests(self):
		for url in self.start_urls:
			yield Request(url, cookies={'getchu_adalt_flag': 'getchu.com'})

	def parse(self, response):
		urls = Selector(response).xpath('//a[@class="adultanime_title"]/@href').extract()
		
		for url in urls:
			yield Request(url, callback=self.parse_list, cookies={'getchu_adalt_flag': 'getchu.com'})

	def parse_list(self, response):
		urls = Selector(response).xpath('//a[@class="blueb"]/@href').extract()
		for url in urls:
			url = 'http://www.getchu.com' + url[2:]
			yield Request(url, callback=self.parse_item, cookies={'getchu_adalt_flag': 'getchu.com'})

	def parse_item(self, response):
		content = Selector(response)
		item = HentaiItem()
		item['title'] = content.xpath('//*[@id="soft-title"]/text()').extract()[0].strip()
		item['price'] = content.xpath('//table[@style="padding:1px;"]/tr[2]/td[2]/text()').extract()[0].strip()
		item['pubtime'] = content.xpath('//*[@id="tooltip-day"]/text()').extract()[0].strip()
		publisher = content.xpath('//*[@id="brandsite"]/text()').extract()
		if len(publisher) == 0:
			publisher = content.xpath('//table[@style="padding:1px;"]/tr[1]/td[2]/text()').extract()
		item['publisher'] = publisher[0].strip()
		code = content.xpath('//table[@style="padding:1px;"]/tr[6]/td[2]/text()').extract()
		if len(code) == 0:
			item['code'] = ''
		else:
			item['code'] = code[0].strip()
		cover = content.xpath('//img[@style="border:0;"]/@src').extract()
		if len(cover) == 0:
			item['cover'] = ''
		else:
			item['cover'] = 'http://www.getchu.com' + cover[0][1:]
		pics = content.xpath('//div[@align="center"]/a/img/@src').extract()
		arr = []
		for pic in pics:
			if pic[0] == '.':
				arr.append('http://www.getchu.com' + pic.strip('.'))
			else:
				arr.append(pic)
		item['pics'] = arr
		item['origin'] = 'getchu'
		con = content.xpath('//div[@id="wrapper"]/div/div[@class="tablebody"]')
		num = len(con.extract())
		item['staff'] = ''
		item['summary'] = ''
		titles = content.xpath('//div[@id="wrapper"]/div/div[@class="tabletitle"]/text()').extract()[:num]
		for title in titles:
			c = con[titles.index(title)]
			if title == '\xa0ストーリー': #故事
				item['summary'] = ''.join(c.xpath('text()').extract()).strip()
				continue
			elif title == '\xa0スタッフ／キャスト': #工作人员/演员
				item['staff'] = ''.join(c.xpath('text()').extract()).strip()
				continue
			elif title == '\xa0商品紹介': 
				item['summary'] = ''.join(c.xpath('text()').extract()).strip()
				continue
			elif title == '\xa0スタッフ': #工作人员
				item['staff'] = ''.join(c.xpath('text()').extract()).strip()
			
		yield item
