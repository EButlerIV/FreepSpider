from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from FreepScraper.items import FreepThread, FreepComment
import re

class FreepThreadSpider(CrawlSpider):
  name = "freepThreads"
  allowed_domains = ["freerepublic.com"]
  start_urls = ["http://www.freerepublic.com/tag/*/index"]
  rules = [Rule(SgmlLinkExtractor(allow=['/tag/\*/index\S+'])), Rule(SgmlLinkExtractor(allow=['/focus/f-\S+']), 'parse_thread')]

  def parse_thread(self, response):
    hxs = HtmlXPathSelector(response)
    threads = hxs.select('//ul/li[contains(@class,"article")]')
    items = []
    thread = FreepThread()
    thread['_id'] = re.findall(r'\d+', str(response))[1]
    thread['title'] = hxs.select('//a[contains(@id,"top")]/font/b/text()').extract()[0]
    thread['tags'] = hxs.select('//a[contains(@href, "tag")]/*[text() != "Browse"]/text()').extract()
    thread['author'] = hxs.select('//small/a[contains(@title, "Since")]/font/b/text()').extract()[0]
    thread['datePosted'] = hxs.select('//small[contains(text(), "Posted on")]/b/span[@class="date"]/text()').extract()[0]
    thread['sourceName'] = hxs.select('//small/b/a[contains(text()," ^")]/text()').extract()[0][:-2]
    thread['sourceURL'] = hxs.select('//small/b/a[contains(text()," ^")]/@href').extract()[0][2:]
    thread['datePosted'] = hxs.select('//text()[preceding-sibling::b/a[contains(text()," ^")]]').extract()[0][4:-1]
    thread['excerpt'] = not not hxs.select('//p[contains(text(),"(Excerpt) Read more at")]/text()').extract()
    thread['threadBody'] = "".join(hxs.select('//p[preceding-sibling::p/small[contains(text(), "Posted on")] and following-sibling::p[contains(text(),"(Excerpt) Read more at")]]//text()').extract())
    items.append(thread)
    replyTo = ['!origin']
    commentNumbers = hxs.select('//a[contains(text(),"")]/@name').extract()[1:]
    commentTexts = hxs.select('//div[@class="b2"]')
    commentPosters = hxs.select('//div[@class="a2"]/a[contains(@href,"~")]/text()').extract()
    commentTimeDates = hxs.select('//div[@class="a2"]/b/span[@class="date"]/text()').extract()

    cleanedTexts = []
    for commenttext in commentTexts:
      cText = "".join(commenttext.select('.//text()').extract())
      cleaned_text = re.sub(ur'(\s)\s+', ur'\1', cText, flags=re.MULTILINE + re.UNICODE)[1:-1]
      cleanedTexts.append(cleaned_text) 
    replyTo.extend(hxs.select('//div[@class="a2"][contains(text(),"To:")]/b/text()').extract())
    tagline = hxs.select('//text()[preceding-sibling::a[contains(@href,"/~")]]').extract()
    
    for num, text, to, tag, timedate, name in map(None, commentNumbers, cleanedTexts, replyTo, tagline, commentTimeDates, commentPosters):
      comment = FreepComment()
      comment['threadId'] = thread['_id']
      comment['commentNumber'] = num
      comment['replyTo'] = to
      comment['commentText'] = text
      if tag == '\n':
        comment['tagline'] = False
      else:
        comment['tagline'] = tag[1:-1]
      comment['poster'] = name
      comment['datePosted'] = timedate.split(' ')[0]
      comment['timePosted'] = timedate.split(' ')[1]
      items.append(comment)
    return items
