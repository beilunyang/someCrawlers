# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.exceptions import DropItem
from crawler.settings import DATABASE
		
class MongoPipeline(object):
	def __init__(self):
		self.client = pymongo.MongoClient(DATABASE['host'], DATABASE['port'])
		db = self.client[DATABASE['db']]
		self.collection = db[DATABASE['collection']]
		self.collection.create_index([('title', pymongo.ASCENDING), ('pubtime', pymongo.ASCENDING), ('publisher', pymongo.ASCENDING), ('price', pymongo.ASCENDING), ('code', pymongo.ASCENDING)], unique=True)

	def close_spider(self, spider):
		self.client.close()

	def process_item(self, item, spider):
		try:
			self.collection.insert(dict(item))
		except pymongo.errors.DuplicateKeyError:
			pass
		return item




