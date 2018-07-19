# -*- coding: utf-8 -*-
import json

import scrapy,re
from ..items import TaobaoItem

class Taobao1Spider(scrapy.Spider):
    name = 'taobao1'
    allowed_domains = ['s.taobao.com','item.taobao.com','rate.taobao.com','taobao.com']
    key = 'oppo'
    page = 1
    start_urls = ['https://s.taobao.com/list?q={}&cat=11%2C1101%2C1201%2C14%2C1512%2C20%2C50008090%2C50012164%2C50018222%2C50018264%2C50019780%2C50076292&style=grid&seller_type=taobao&spm=a219r.lm872.1000187.1'.format(key)]
    urls = 'https://s.taobao.com/list?q={}&cat=11%2C1101%2C1201%2C14%2C1512%2C20%2C50008090%2C50012164%2C50018222%2C50018264%2C50019780%2C50076292&style=grid&seller_type=taobao&spm=a219r.lm872.1000187.1&s={}'

    # https://s.taobao.com/list?q=oppo
    # https://s.taobao.com/list?q=oppo&bcoffset=12&s=60
    # 评论接口
    # https://rate.taobao.com/feedRateList.htm?auctionNumId=565197510638&userNumId=1986869048&currentPageNum=2&pageSize=20&rateType=&orderType=sort_weight

    # 获取店铺url
    def parse(self, response):
        url_compile = re.compile(r'"comment_url":"(.*?)",')
        url_list = url_compile.findall(response.text)
        i = 1
        for url in url_list:
            url = 'https:' + url.encode('latin1').decode('unicode_escape')
            print('进入第%d个店' % i)
            i += 1
            yield scrapy.Request(url, callback=self.parse_detail)
            print('完成第%d个店' % i)
        if self.page <= 100:
            self.page += 1
            url = self.urls.format(self.key,str((self.page-1)*60))
            yield scrapy.Request(url=url, callback=self.parse)
    # 获取评论接口所需的id和店铺Id,拼接评论接口url
    def parse_detail(self,response):
        content = response.xpath('//meta[@name="microscope-data"]/@content')[0].extract()
        item = TaobaoItem()
        Id = response.xpath('//ul/li[@class="tb-social-fav"]/a/@href')[0].extract()
        Id = Id.split('=')[-1]
        print('店铺ID:%s'%Id)
        item['shopId'] = content.split(';')[3].split('=')[-1]
        start_page = 1
        end_page = 10
        for page in range(start_page,end_page+1):
            user_evaluation_url ='https://rate.taobao.com/feedRateList.htm?auctionNumId={}&userNumId=1986869048&currentPageNum={}&pageSize=20&rateType=&orderType=sort_weight'.format(Id,page)
            print('获取评论第%d页'%page)
            yield scrapy.Request(user_evaluation_url, callback=self.parse_detail2,meta={'items': item})
            print('完成获取评论第%d页' % page)
    # 获取评论信息
    def parse_detail2(self, response):
        item = response.meta['items']
        user_com = json.loads(response.text.strip('\r\n()'))
        for user in user_com['comments']:
            item['com_date'] = user['date']
            item['com_text'] = user['content']
            item['com_user_name'] = user['user']['nick']
            item['com_user_lv'] = user['user']['vipLevel']
            item['kw'] = self.key
            yield item