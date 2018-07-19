# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql,pymongo
from scrapy.utils.project import get_project_settings

class TaobaoPipeline(object):
    def open_spider(self,spider):
        settings = get_project_settings()
        host = settings['HOST']
        port = settings['PORT']
        user = settings['USER']
        password = settings['PASSWORD']
        dbname = settings['DBNAME']
        charset = settings['CHARSET']
        # 链接数据库
        self.conn = pymysql.connect(host=host, port=port, user=user, password=password, db=dbname, charset=charset)
        # 获取游标
        self.cursor = self.conn.cursor()
    def process_item(self, item, spider):
        # 执行sql语句，写入到数据库中
        # 拼接sql语句
        sql = 'insert into taobao_commit(kw,shopId, com_user_name, com_user_lv, com_date, com_text) values("%s","%s","%s","%s","%s","%s")' % (item['kw'],item['shopId'], item['com_user_name'], item['com_user_lv'], item['com_date'], item['com_text'])
        # 简单去重
        quit_text = [
            '评价方未及时做出评价,系统默认好评!',
            '此用户没有填写评价。',
            '15天内买家未作出评价',
        ]
        if not item['com_text'] in quit_text:
            # 执行sql语句
            try:
                self.cursor.execute(sql)
                # 提交一下
                self.conn.commit()
            except Exception as e:
                print('*' * 100)
                print(e)
                print('*' * 100)
                # 回滚
                self.conn.rollback()
            return item
        else:
            print('该评论没有意义')
    def close_spider(self, spider):
        #关闭游标
        self.cursor.close()
        # 关闭数据库
        self.conn.close()


class TaobaoMDBPipeline(object):
    def open_spider(self,spider):
        # 连接MongoDB
        self.client = pymongo.MongoClient(host='localhost',port=27017)
        # 获取数据库
        self.db = self.client['taobao']
        self.collection= self.db['taobao_commit']
    def process_item(self, item, spider):
        # 插入数据

        result = self.collection.insert_one(dict(item))
        # print(result)
        return item
    def close_spider(self,spider):
        self.client.close()