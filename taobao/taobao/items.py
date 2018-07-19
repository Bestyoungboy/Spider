# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TaobaoItem(scrapy.Item):
    kw = scrapy.Field()
    shopId = scrapy.Field()
    com_date = scrapy.Field()
    com_user_name = scrapy.Field()
    com_user_lv = scrapy.Field()
    com_text = scrapy.Field()
