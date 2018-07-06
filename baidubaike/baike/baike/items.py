# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BaikeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 一级标题
    level1Title = scrapy.Field()
    # 二级标题
    level2Title = scrapy.Field()
    # 描述
    content = scrapy.Field()
