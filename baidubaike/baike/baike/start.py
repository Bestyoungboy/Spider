import scrapy.cmdline


def main():
    scrapy.cmdline.execute(['scrapy', 'crawl', 'mybaike'])


if __name__ == '__main__':
    main()
