# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

import pymongo

from scrapy.exceptions import DropItem
from scrapy.conf import settings
from scrapy import log

from FreepScraper.items import FreepThread, FreepComment

class FreepscraperPipeline(object):
    def process_item(self, item, spider):
        return item

class MongoDBPipeline(object):
    def __init__(self):
        connection = pymongo.Connection(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.threadCollection = db[settings['THREAD_COLLECTION']]
        self.commentCollection = db[settings['COMMENT_COLLECTION']]
        
    def process_item(self, item, spider):
    	valid = True
        for data in item:
          # here we only check if the data is not null
          # but we could do any crazy validation we want
       	  if not data:
            valid = False
            raise DropItem("Missing %s of blogpost from %s" %(data, item['url']))
        if valid:
          if isinstance(item, FreepThread):
            self.collection = self.threadCollection
            print 'is a thread'
          if isinstance(item, FreepComment):
            self.collection = self.commentCollection
            print 'is a comment'
          self.collection.insert(dict(item))
          log.msg("Item wrote to MongoDB database %s/%s" %
                  (settings['MONGODB_DB'], str(self.collection)),
                  level=log.DEBUG, spider=spider) 
        return item
