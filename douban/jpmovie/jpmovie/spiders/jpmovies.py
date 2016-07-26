# -*- coding: utf-8 -*-
from scrapy import log
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from jpmovie.items import JpmovieItem 

class JpmovieSpider(CrawlSpider):
    name = "jpmovies"
    allowed_domains = ["movie.douban.com"]
    start_urls = (
        'https://movie.douban.com/tag/%E6%97%A5%E6%9C%AC%20%E7%94%B5%E5%BD%B1?start=0&type=T',
    )

    rules = (
            Rule(LinkExtractor(allow=r'https://movie.douban.com/subject/\d+?/'), callback='parse_item'),
            Rule(LinkExtractor(restrict_xpaths='//*[@class="next"]')),
        )

    def zero(self, array):
    	if len(array):
    		return array[0]
    	else:
    		return ''

    def parse_item(self, response):
        try:
            item = JpmovieItem()
            se = response.selector
            info = se.xpath('//*[@id="info"]')
            item['title'] = se.xpath('//h1/span[1]/text()').extract()[0]
            item['cover'] = self.zero(se.xpath('//img[@rel="v:image"]/@src').extract())
            item['intro'] = '\n'.join(map(lambda str:str.strip(), se.xpath('//*[@property="v:summary"]/text()').extract()))
            item['directors'] = info.xpath('.//*[@rel="v:directedBy"]/text()').extract()
            item['writers'] = info.xpath('span[2]/span[2]/a/text()').extract()
            item['actors'] = info.xpath('.//*[@rel="v:starring"]/text()').extract()
            item['types'] = info.xpath('*[@property="v:genre"]/text()').extract()
            item['released'] = info.xpath('*[@property="v:initialReleaseDate"]/text()').extract()
            item['mins'] = self.zero(info.xpath('*[@property="v:runtime"]/text()').extract())
        	# 只返回子表达式
            alias = se.re(r'<span class="pl">又名:</span>((.|\s)+?)<br>')
            if len(alias):
                item['alias'] = alias[0].strip().split('/')
            else:
                item['alias'] = []
            imdb = info.re(r'http://www.imdb.com/title/(\w+?)"')
            if len(imdb):
                item['imdb'] = imdb[0].strip()
            else:
                item['imdb'] = ''
            return item
        except Exception as e:
            print('parse error', e)

