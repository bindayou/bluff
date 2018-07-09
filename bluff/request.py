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


async def fetch(url, spider, session, semaphore):
    with (await semaphore):
        try:
            if callable(spider.headers):
                headers = spider.headers()
            else:
                headers = spider.headers
            async with session.get(url, headers=headers, proxy=spider.proxy) as response:
                if response.status in [200, 201]:
                    return await response.text()
                return None
        except TypeError as e:
            return None
