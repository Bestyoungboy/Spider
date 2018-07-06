import requests
from bs4 import BeautifulSoup

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}


def start_url(url):
    res = requests.get(url, headers=header)
    html = res.text
    soup = BeautifulSoup(html, 'html5lib')
    # '//b[@class="top"]/a/@href'
    books_list = soup.findAll('li', class_="fenlei")
    print(books_list)


if __name__ == '__main__':
    url = 'http://chuangshi.qq.com/bk/'
    start_url(url)
