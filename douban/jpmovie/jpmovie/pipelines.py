# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.exceptions import DropItem
from jpmovie.settings import DATABASE
		
class MongoPipeline(object):
	def __init__(self):
		self.client = pymongo.MongoClient(DATABASE['host'], DATABASE['port'])
		db = self.client[DATABASE['db']]
		self.collection = db[DATABASE['collection']]
		self.collection.create_index([('title', pymongo.ASCENDING)], unique=True)

	def close_spider(self, spider):
		self.client.close()

	def process_item(self, item, spider):
		try:
			newitem = dict(item)
			del newitem['image_urls']
			for image in newitem['images']:
				del image['checksum']
			self.collection.insert(newitem)
		except pymongo.errors.DuplicateKeyError:
			print('duplicateKeyError')
		return item




