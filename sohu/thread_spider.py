#!/usr/bin/env python3.6
# coding: utf-8

import sys
import time
from queue import Queue
from threading import Thread
from urllib.parse import urlparse

import requests
from lxml import etree

'''
    解耦

    线程1 -> 结果 -> 线程3 ->
    线程2 -> 结果 -> 线程2 ->
    线程3 -> 结果 -> 线程7
    .
    .
    .
    线程10 -> 结果 -> 线程20


    线程 A
    1. 启动
    2. 检查“待抓取的 URL 列表”
    3. 取出一条数据
    4. 抓取
    5. 解析
    6. 清洗、去重
    7. 将新的 URL 添加到“待抓取 URL 列表”
'''

IDLE = 0     # 空闲状态
WORKING = 1  # 工作状态

REQUESTED_URL = set()  # 抓取过的 URL


class retry(object):
    def __init__(self, max_retries=3, wait=0, exceptions=(Exception,)):
        self.max_retries = max_retries
        self.exceptions = exceptions
        self.wait = wait

    def __call__(self, f):
        def wrapper(*args, **kwargs):
            for i in range(self.max_retries + 1):
                try:
                    result = f(*args, **kwargs)
                except self.exceptions as e:
                    print('waitting', e)
                    time.sleep(self.wait)
                    print('retry %s' % (i + 1))
                    continue
                else:
                    return result
        return wrapper


@retry(3, 3)
def fetch(url):
    '''页面下载'''
    print(f'Fetching: {url}')
    resp = requests.get(url)
    REQUESTED_URL.add(url)  # 添加访问记录
    if resp.status_code == 200:
        return resp.text
    return None


def parse(html):
    '''页面解析'''
    if html in [None, '', b'']:
        return []
    # xpath 过滤 a 标签
    doc = etree.HTML(html)
    if doc is None:
        return []
    urls = doc.xpath('//a/@href')

    # 清洗、规范化
    url_list = []
    # 筛选 /ch/42?_f=m-index_game_pd 类型的链接
    for ori_url in urls:
        parsed_url = urlparse(ori_url)
        domain = parsed_url.netloc.strip() or 'm.sohu.com'
        if domain == 'm.sohu.com':
            scheme = parsed_url.scheme.strip() or 'http'
            if scheme in ['http', 'https']:
                path = parsed_url.path.strip()
                query = f'?{parsed_url.query}'.strip() if parsed_url.query else ''
                url = f'{scheme}://{domain}{path}{query}'
                url_list.append(url)
    return url_list


class Spider(Thread):
    def __init__(self, todo_list):
        super().__init__()
        self.setDaemon(True)
        self.todo_list = todo_list
        self.stat = IDLE

    def is_idle(self):
        return self.stat == IDLE

    def run(self):
        while True:
            url = self.todo_list.get()

            # 开始抓取过程
            self.stat = WORKING          # 修改为工作状态
            html = fetch(url)            # 抓取
            url_list = set(parse(html))  # 解析
            url_list -= REQUESTED_URL    # 去重 (TODO: 更严格的去重)

            # 将新得到的 URL 循环添加到 TODO_LIST
            for url in url_list:
                self.todo_list.put(url)

            # 修改为空闲状态
            self.stat = IDLE


def is_all_spider_in_idle(spiders):
    '''检查所有爬虫是否为空闲状态'''
    all_status = [spd.is_idle() for spd in spiders]
    return all(all_status)


def main(max_threads):
    # 添加初始任务
    print('Start')
    todo_list = Queue()  # 待抓取的 URL
    todo_list.put('http://m.sohu.com/')

    # 创建 N 个线程，并启动
    print('Spawn spiders')
    spiders = [Spider(todo_list) for i in range(max_threads)]
    for spd in spiders:
        spd.start()

    # 循环检查是否已经完成全部工作
    while True:
        if todo_list.empty() and is_all_spider_in_idle(spiders):
            # 仅当待抓取列表为空且所有爬虫为空闲状态时，程序退出
            print('All works done, exit')
            sys.exit(0)
        else:
            print('Requested %s' % len(REQUESTED_URL))
            time.sleep(1)


if __name__ == '__main__':
    if len(sys.argv) >= 2:
        max_threads = int(sys.argv[1])
        main(max_threads)
    else:
        print('请输入参数')
