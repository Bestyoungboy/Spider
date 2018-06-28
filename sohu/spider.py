#!/usr/bin/env python3.6
# coding: utf-8

import time
from queue import Queue
from threading import Thread
from urllib.parse import urlparse

import requests
from lxml import etree


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

REQUESTED_URL = set()


@retry(3, 3)
def fetch(url):
    '''页面下载'''
    print(f'Fetching: {url}')
    resp = requests.get(url)
    REQUESTED_URL.add(url)  # 添加访问记录
    if resp.status_code >= 300:
        return None
    else:
        return resp.text


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
            path = parsed_url.path.strip()
            query = f'?{parsed_url.query}'.strip() if parsed_url.query else ''
            url = f'{scheme}://{domain}{path}{query}'
            url_list.append(url)
    return url_list


def get_and_parse(url, url_queue):
    '''下载后解析'''
    html = fetch(url)
    for url in parse(html):
        url_queue.put(url)


def process(url_list):
    queue = Queue()  # 抓取结果存放的队列

    workers = []  # 用来抓取的线程的列表
    for url in url_list:
        t = Thread(target=get_and_parse, args=(url, queue))
        t.setDaemon(True)
        workers.append(t)
        t.start()

    for t in workers:
        t.join()  # 确保每个线程都能正常结束

    return list(queue.queue)


if __name__ == '__main__':
    url_list = ['http://m.sohu.com/']

    while url_list:
        print('Requested %s' % len(REQUESTED_URL))
        url_list = set(url_list) - REQUESTED_URL  # url 去重
        url_list = process(url_list)
