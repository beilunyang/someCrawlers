import pymongo
from scrapy.exceptions import DropItem
from crawler.settings import DATABASE

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
			self.collection.insert(newitem)
		except pymongo.errors.DuplicateKeyError:
			print('duplicateKeyError')
		return item