# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from flask_doc.items import FlaskDocItem

class FlaskSpider(CrawlSpider):
    name = 'flask'
    allowed_domains = ['flask.pocoo.org']
    start_urls = ['http://flask.pocoo.org/docs/1.0/']

    rules = (
            Rule(LinkExtractor(allow=r'http://flask.pocoo.org/docs/1.0/.*'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        i = FlaskDocItem()
        i['url'] = response.url
        i['text'] = ' '.join(response.xpath('//text()').extract())
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        return i
