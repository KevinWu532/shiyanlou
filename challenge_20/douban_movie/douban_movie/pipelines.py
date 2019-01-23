# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import redis, json
from scrapy.exceptions import DropItem

class DoubanMoviePipeline(object):
    def process_item(self, item, spider):
        item['score'] = int(item['score'])
        if item['score'] < 8:
            raise DropItem('score < 8')
        else:
            self.redis.lpush('douban_movie:items', json.dumps(dict(item)))
            return item
    
    def open_spider(self, spider):
        self.redis = redis.StrictRedis(host='localhost', port=6379,db=0)
