# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class FreepThread(Item):
  _id = Field()
  title = Field()
  tags = Field()
  author = Field()
  datePublished = Field()
  sourceName = Field()
  sourceURL = Field()
  excerpt = Field()
  threadBody = Field()
  datePosted = Field()
  pass

class FreepComment(Item):
  threadId = Field()
  commentNumber = Field()
  replyTo = Field()
  commentText = Field()
  poster = Field()
  datePosted = Field()
  timePosted = Field()
  tagline = Field()

class FreepUser(Item):
  name = Field()
  registrationDate = Field()
