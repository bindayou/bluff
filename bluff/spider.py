# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     spider
   Description :
   date：          6/28/18
-------------------------------------------------
   Change Activity:
                   6/28/18:
-------------------------------------------------
"""
# Python standard library module
import asyncio
import re
# Python third party module
import aiohttp
# Application custom module
from bluff.request import fetch
from bluff.core import CrawlerCore


class Spider(CrawlerCore):
    start_url = ''
    base_url = None
    parsers = []
    error_urls = []
    urls_count = 0
    concurrency = 5
    interval = None
    headers = {}
    proxy = None
    cookie_jar = None

    @classmethod
    def _is_running(cls):
        is_running = False
        for parser in cls.parsers:
            if not parser.pre_parse_urls.empty() or len(parser.parsing_urls) > 0:
                is_running = True
        return is_running

    @classmethod
    def _parse(cls, html):
        for parser in cls.parsers:
            parser._parse_urls(html, cls.base_url)

    @classmethod
    def flow(cls):
        if cls.base_url is None:
            cls.base_url = re.match(
                '(http|https)://[\w\-_]+(\.[\w\-_]+)+/',
                cls.start_url).group()
            cls.info(f'Base url: {cls.base_url}')
        try:
            semaphore = asyncio.Semaphore(cls.concurrency)
            tasks = asyncio.wait([parser.task(cls, semaphore)
                                  for parser in cls.parsers])
            cls._loop.run_until_complete(cls._init_parse(semaphore))
            cls._loop.run_until_complete(tasks)
        except KeyboardInterrupt as e:
            for task in asyncio.Task.all_tasks():
                task.cancel()
            cls._loop.run_forever()
        finally:
            for parser in cls.parsers:
                if parser.item is not None:
                    cls.info(
                        f'Item "{parser.item.name}": {parser.item.count}')
            cls.info(f'Requests count: {cls.urls_count}')
            cls.info(f'Error count: {cls.error_urls}')
            cls._loop.close()

    @classmethod
    async def _init_parse(cls, semaphore):
        async with aiohttp.ClientSession(cookie_jar=cls.cookie_jar) as session:
            html = await fetch(cls.start_url, cls, session, semaphore)
            cls._parse(html)
Spider.run()