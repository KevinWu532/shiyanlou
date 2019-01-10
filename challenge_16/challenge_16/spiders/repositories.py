# -*- coding: utf-8 -*-
import scrapy
from challenge_16.items import RepositoriesItem

class RepositoriesSpider(scrapy.Spider):
    name = 'repositories'
    allowed_domains = ['github.com']
    start_urls = ['http://github.com/']
    
    def start_requests(self):
        temp = (
                'https://github.com/shiyanlou?tab=repositories',
                'https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK5MjAxNy0wNi0wN1QwNjoyMToxMCswODowMM4FkpVn&tab=repositories',
                'https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK5MjAxNS0wMS0yNlQxMTozMDoyNSswODowMM4Bx2JQ&tab=repositories',
                'https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK5MjAxNC0xMS0yMVQxODowOTowMiswODowMM4BnQBZ&tab=repositories'
                )
        for url_temp in temp:
            urls = (url_temp.format(i) for i in range(1,31))
            for url in urls:
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for repositories in response.css('div[class="col-9 d-inline-block"]'):
            yield RepositoriesItem({
                'name':repositories.xpath('.//h3/a/text()').re_first('\n        (.+)'),
                'update_time':repositories.xpath('.//relative-time/@datetime').extract_first()
                })
