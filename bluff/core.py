# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     core
   Description :
   date：          7/14/18
-------------------------------------------------
   Change Activity:
                   7/14/18:
-------------------------------------------------
"""

# Python standard library module
import asyncio
import re
# Python third party module
try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError as e:
    pass
import aiohttp
# Application custom module
from bluff.log import LogMixin
from bluff.utils import (
    timeit,
    normal_headers
)
from bluff.request import fetch


class BaseCore(type):
    """
    base core base on metaclass
    """
    def __new__(cls, class_name, objects, name_space):
        # register mixin_class
        objects = cls.register_objects(objects=objects)
        # register base_attrx
        name_space = cls.register_namespace(namespace=name_space)
        return type.__new__(cls, class_name, objects, name_space)

    @staticmethod
    def register_objects(objects):
        if objects:
            new_objects = list(objects)
            new_objects.append(LogMixin)
            objects = tuple(new_objects)
        else:
            objects = (LogMixin,)
        return objects

    @staticmethod
    def register_namespace(namespace):
        namespace["_loop"] = asyncio.get_event_loop()
        return namespace


class CrawlerCore(metaclass=BaseCore):
    """
    crawler core
    you must be implement function flow then execute function run
    """
    @classmethod
    def flow(cls):
        raise NotImplementedError

    @classmethod
    def headers(cls):
        cls.headers = normal_headers()

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
    async def _init_parse(cls, semaphore):
        async with aiohttp.ClientSession(cookie_jar=cls.cookie_jar) as session:
            html = await fetch(cls.start_url, cls, session, semaphore)
            cls._parse(html)

    @classmethod
    def extract_base_url(cls):
        """
        extracting base_url according to start_url
        :return:
        """
        cls.base_url = re.match(
            '(http|https)://[\w\-_]+(\.[\w\-_]+)+/',
            cls.start_url).group()
        cls.info(f'Base url: {cls.base_url}')

    @classmethod
    def close(cls):
        """
        close loop and connection
        :return:
        """
        cls._loop.close()

    @classmethod
    def run(cls):
        @timeit(obj=cls)
        def flow():
            cls.flow()
        flow()
        cls.close()
