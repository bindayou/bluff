# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     request
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
try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    pass
# Application custom module
from .log import logger


async def fetch(url, spider, session, semaphore):
    with (await semaphore):
        try:
            if callable(spider.headers):
                headers = spider.headers()
            else:
                headers = spider.headers
            async with session.get(url, headers=headers, proxy=spider.proxy) as response:
                if response.status in [200, 201]:
                    data = await response.text()
                    return data
                logger.error('Error: {} {}'.format(url, response.status))
                return None
        except BaseException:
            return None
