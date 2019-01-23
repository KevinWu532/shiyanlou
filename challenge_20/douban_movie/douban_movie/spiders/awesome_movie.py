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
            Rule(LinkExtractor(allow=r'https://movie.douban.com/subject/.*/?from=subject-page'), callback='parse_page', follow=True),
    )

    def parse_movie_item(self, response):
        i = MovieItem()
        i['url'] = response.url
        i['name'] = response.xpath('//div[@id="content"]/h1/span[@property="v:itemreviewed"]/text()').extract_first()
        i['summary'] = response.xpath('//span[@property="v:summary"]/text()').re_first(r'\n*\s*(.*)\n*')
        i['score'] = response.css('div#interest_sectl').xpath('.//strong/text()').extract_first()
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        return i

    def parse_start_url(self, response):
        yield self.parse_movie_item(response)

    def parse_page(self, response):
        yield self.parse_movie_item(response)
