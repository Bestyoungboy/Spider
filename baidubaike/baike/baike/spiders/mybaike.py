# -*- coding: utf-8 -*-
import scrapy


class MybaikeSpider(scrapy.Spider):
    name = 'mybaike'
    allowed_domains = ['baike.baidu.com']
    start_urls = ['http://baike.baidu.com/item/python/407313']

    def parse(self, response):
        level1Title = response.xpath('//dd[@class="lemmaWgt-lemmaTitle-title"]/h1/text()')[0].extract()
        level2Title = response.xpath('//dd[@class="lemmaWgt-lemmaTitle-title"]/h2/text()')[0].extract()
