'''
@Software: PyCharm
-- coding: utf-8 -- 
@Time : 2018/5/30 11:50
@Author : ice cream 
@File : doubleColorBall.py
'''

import random, datetime, re
from urllib import request
from bs4 import BeautifulSoup


# 启动展示界面
print('*****欢迎使用千雪彩票软件*****')
print('  - '+datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' -')
print('   * 此系统预测功能仅供娱乐 *')
print('   * 不做为任何实际购买参考 *')
print('   * 中奖信息均采自500.com  *')
print('\n****************************')


# 功能
print('输入"Start"启动软件功能:', end=' ')
while True:
    # 启动指令输入 并进行判断
    start_s = input().lower()
    # 指令正确
    if start_s == 'start':
        print('输入对应功能序号开启功能：')

        # 功能的指令进行判断
        while True:
            features = input('1.查询功能：\n'
                             '2.预测功能：\n')
            # 查询功能
            if features == '1':
                # 爬取 500彩票网
                def url_open(url):
                    req = request.Request(url)
                    res = request.urlopen(req)
                    soup = BeautifulSoup(res.read().decode('gbk'), 'html.parser')
                    return soup

                def handle_url(soup):
                    temp = {}
                    # 获取所查询的彩票开奖期数
                    periods_list = soup.select('a font')
                    for k in periods_list:
                        periods = (k.get_text()).strip()
                        print('第'+periods+'期中奖号码：')

                    print('(注：前六个数字为红球号码,最后一个数字为蓝球号码)')
                    # 中奖号码
                    print('*********************')
                    prize_num = soup.select('.ball_box01 ul li')
                    for num in prize_num:
                        print(num.get_text(), end=' ')

                    # 开奖详情
                    print('\n*********************')
                    prize_infoList = soup.find_all('tr', align=re.compile('center'))[1:]
                    print('\n开奖详情：')
                    for prize in prize_infoList:
                        print((prize.get_text()).split())

                    # 获取开奖、兑奖时间
                    print('\n*********************')
                    open_close = soup.select('.td_title01 span')
                    time_list = open_close[1].get_text().split(" ")
                    for time in time_list:
                        print(time)


                # 启动爬虫并解析数据
                def start_q(url):
                    soup = url_open(url)
                    handle_url(soup)

                # 查询功能细分
                while True:
                    num = input('1.查询最新开奖信息：\n'
                                '2.查询指定期数信息：\n')
                    # 最新开奖信息获取
                    if num == '1':
                        url = 'http://kaijiang.500.com/ssq.shtml'
                        start_q(url)
                        break

                    # 指定查询期数
                    elif num == '2':
                        while True:
                            snum = input('请输入要查询的期数：')
                            # 使用try方法 避免输入期数错误导致程序运行报错 并在出错时提示报错
                            try:
                                url = 'http://kaijiang.500.com/shtml/ssq/%s.shtml?' % snum
                                start_q(url)
                                break
                            except:
                                print('输入的期数不正确请重新输入')
                        break
                    else:
                        print('输入的指令有误,请重新输入')

                break

            # 预测功能
            elif features == '2':
                print('-- 是否进行中奖号码预测? ->')
                while True:
                    enter = (input('  (请输入"Y(继续)/N(退出)")：')).lower()
                    if enter == 'y':
                        print('\n****************************')
                        print('\n   预测下期中奖号码为：')
                        ball_list = []
                        for i in range(1, 34):
                            if i < 10:
                                i = "0" + str(i)
                                ball_list.append(i)

                            else:
                                i = str(i)
                                ball_list.append(i)

                        h = random.sample(ball_list, 6)
                        for s in h:
                            print(s, end=' ')

                        luckyBall = random.randint(1, 16)
                        if luckyBall < 10:
                            luckyBall = '0' + str(luckyBall)
                        else:
                            luckyBall = str(luckyBall)
                        print(luckyBall)
                        print('\n   -* 祝您喜中大奖 *-')
                        break
                    elif enter == 'n':
                        print('    退出彩票预测系统')
                        break
                    else:
                        print('输入指令有误,请重新输入')
                break
            else:
                print('输入指令有误,请重新输入:')
        break
    else:
        print('输入指令有误,请重新输入:', end='')


print('\n   -* 欢迎下次使用 *-')
print('\n****************************')
