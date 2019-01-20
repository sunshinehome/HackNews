# -*- coding: utf-8 -*-
import random

import scrapy
import re

from hackerNews.items import HackernewsItem


class DaynewsSpider(scrapy.Spider):
    name = 'DayNews'
    allowed_domains = ['search.freebuf.com']


    def start_requests(self):
        base_urls='http://search.freebuf.com/search/find/?year=2018&score=0&articleType=0&origin=0&tabType=1&content=&page='
        for i in range(1,607):
            start_urls=base_urls+str(i)
            yield scrapy.Request(start_urls)

    def parse(self, response):
        pattern = re.compile('"url":(.*?),"imgUrl":(.*?),"title":(.*?),"content":(.*?),"time":(.*?),"type":(.*?),"name":(.*?),', re.S)
        items = re.findall(pattern, response.body.decode('utf-8'))
        itemlist=HackernewsItem()
        for item in items:
            itemlist['url']=item[0]
            itemlist['title']=item[2]
            itemlist['content']=item[3]
            itemlist['time']=item[4]
            itemlist['author']=item[6]
            yield itemlist





