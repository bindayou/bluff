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
from datetime import datetime
# Python third party module
import aiohttp
try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    pass
# Application custom module
from .request import fetch
from .log import logger


class Spider:
    start_url = ''
    base_url = None
    parsers = []
    error_urls = []
    urls_count = 0
    concurrency = 5
    interval = None  # Todo: Limit the interval between two requests
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
    def run(cls):
        logger.info('Spider starting!')
        start_time = datetime.now()
        _loop = asyncio.get_event_loop()

        if cls.base_url is None:
            cls.base_url = re.match(
                '(http|https)://[\w\-_]+(\.[\w\-_]+)+/',
                cls.start_url).group()
            logger.info(f'Base url: {cls.base_url}')
        try:
            semaphore = asyncio.Semaphore(cls.concurrency)
            tasks = asyncio.wait([parser.task(cls, semaphore)
                                  for parser in cls.parsers])
            _loop.run_until_complete(cls._init_parse(semaphore))
            _loop.run_until_complete(tasks)
        except KeyboardInterrupt:
            for task in asyncio.Task.all_tasks():
                task.cancel()
            _loop.run_forever()
        finally:
            end_time = datetime.now()
            for parser in cls.parsers:
                if parser.item is not None:
                    logger.info(
                        f'Item "{parser.item.name}": {parser.item.count}')
            logger.info(f'Requests count: {cls.urls_count}')
            logger.info(f'Error count: {cls.error_urls}')
            logger.info(f'Time usage: {end_time - start_time}')
            logger.info('Spider finished!')
            _loop.close()

    @classmethod
    async def _init_parse(cls, semaphore):
        async with aiohttp.ClientSession(cookie_jar=cls.cookie_jar) as session:
            html = await fetch(cls.start_url, cls, session, semaphore)
            cls._parse(html)
