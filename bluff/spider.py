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
# Python third party module
# Application custom module
from bluff.core import CrawlerCore


class Spider(CrawlerCore):
    start_url = ''
    base_url = None
    parsers = []
    error_urls = []
    urls_count = 0
    concurrency = 5
    interval = None
    proxy = None
    cookie_jar = None

    @classmethod
    def flow(cls):
        if cls.base_url is None:
            cls.extract_base_url()
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
