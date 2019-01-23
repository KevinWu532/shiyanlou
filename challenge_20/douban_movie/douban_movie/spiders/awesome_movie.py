# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from douban_movie.items import MovieItem

class AwesomeMovieSpider(CrawlSpider):
    name = 'awesome-movie'
    
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/subject/3011091/']

    rules = (
            Rule(LinkExtractor(allow=r'https://movie.douban.com/subject/.*/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        i = MovieItem()
        i['url'] = response.url
        i['name'] = response.xpath('//div[@id="content"]/h1/span[@property="v:itemreviewed"]/text()').extract()
        i['summary'] = ''.join(response.xpath('//div[@id="link-report"]/span[@class="all hidden"]/text()').re(r'\n*\s*(.*)\n*'))
        i['score'] = response.css('div#interest_sectl').xpath('.//strong/text()').extract_first()
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        return i
