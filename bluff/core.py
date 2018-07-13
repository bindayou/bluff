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
# Python third party module
try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError as e:
    pass
# Application custom module
from bluff.log import LogMixin
from bluff.utils import timeit


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
    def run(cls):
        @timeit(obj=cls)
        def flow():
            cls.flow()
        flow()
