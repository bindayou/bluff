# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     utils
   Description :
   date：          7/10/18
-------------------------------------------------
   Change Activity:
                   7/10/18:
-------------------------------------------------
"""
# Python standard library module
import time
from functools import wraps


def timeit(obj):
    """
    statistical run time -- this is the highest level
    :param obj:
    :return:
    """
    def wrapper(origin_func):
        @wraps(origin_func)
        def _wrapper(*args, **kwargs):
            start_time = time.time()
            obj.info("Crawler-Start")
            try:
                origin_func(*args, **kwargs)
            except Exception as e:
                obj.info(e)
            obj.info("Crawler-End")
            end_time = time.time()
            obj.info(f"Crawler-CountTime:{str(end_time-start_time)[:5]}s")
        return _wrapper
    return wrapper
