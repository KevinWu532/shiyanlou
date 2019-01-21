# -*- coding: utf-8 -*-
import scrapy
from shiyanlougithub.items import ShiyanlougithubItem

class SsSpider(scrapy.Spider):
    name = 'ss'
    start_urls = ['https://github.com/shiyanlou?tab=repositories']

    def parse(self, response):
        for li in response.xpath('//div[@class="col-9 d-inline-block"]'):
           item = ShiyanlougithubItem()
           item['name']=li.xpath('.//h3/a/text()').re_first('\n        (.+)')
           item['update_time']=li.xpath('.//relative-time/@datetime').extract_first()
           li_url = response.urljoin(li.xpath('.//h3/a/@href').extract_first())
           request = scrapy.Request(li_url, callback=self.li_parse)
           request.meta['item'] = item
           yield request
        
        for x in response.xpath('//div[@class="pagination"]/a'):
            text = x.xpath('.//text()').extract_first()
            if text == 'Next':
                next_url = x.xpath('.//@href').extract_first()
                yield response.follow(next_url, callback=self.parse)
            

    def li_parse(self, response):
        item = response.meta['item']
        for x in response.xpath('//div/ul[@class="numbers-summary"]/li'):
            text = x.xpath('.//a/text()').re_first(r'\n\s*(.*)\n')
            number = x.xpath('.//span/text()').re_first(r'\n\s*(.*)\n')
            if text and number:
                number = number.replace(',','')
                if text in ('commit', 'commits'):
                    item['commits'] = int(number)
                if text in ('branch', 'branches'):
                    item['branches'] = int(number)
                if text in ('release', 'releases'):
                    item['releases'] = int(number)
        yield item
