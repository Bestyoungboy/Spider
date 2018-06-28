# -*- coding: utf-8 -*-
import scrapy


class MybaikeSpider(scrapy.Spider):
    name = 'mybaike'
    allowed_domains = ['baike.baidu.com']
    start_urls = ['http://baike.baidu.com/']

    def parse(self, response):
        pass
