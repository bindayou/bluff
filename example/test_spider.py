# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     test_spider
   Description :
   date：          6/28/18
-------------------------------------------------
   Change Activity:
                   6/28/18:
-------------------------------------------------
"""
import sys
sys.path.append("/home/linhanqiu/Proj/bluff/")
from bluff import Css, Item, Parser, Spider


class Post(Item):
    title = Css('.ph')

    async def save(self):
        print(self.title)


class MySpider(Spider):
    start_url = 'http://blog.sciencenet.cn/home.php?mod=space&uid=40109&do=blog&view=me&from=space'
    concurrency = 1
    headers = {'User-Agent': 'Google Spider'}
    parsers = [
        Parser('http://blog.sciencenet.cn/home.php\?mod=space&uid=\d+&do=blog&view=me&from=space&amp;page=\d+'),
        Parser(
            'blog\-\d+\-\d+\.html',
            Post)]


MySpider.run()
