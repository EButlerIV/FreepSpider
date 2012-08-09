# Scrapy settings for FreepScraper project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'FreepScraper'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['FreepScraper.spiders']
NEWSPIDER_MODULE = 'FreepScraper.spiders'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

ITEM_PIPELINES = ['FreepScraper.pipelines.MongoDBPipeline',]

MONGODB_SERVER = "localhost"
MONGODB_PORT = 27017
MONGODB_DB = "freep"
THREAD_COLLECTION = "threads"
COMMENT_COLLECTION = 'comments'
