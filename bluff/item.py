# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     item
   Description :
   date：          6/28/18
-------------------------------------------------
   Change Activity:
                   6/28/18:
-------------------------------------------------
"""

# Python standard library module
from html import unescape
# Application custom module
from bluff.log import LogMixin
from bluff.selector import Selector


class ItemType(type):
    def __new__(mcs, name, bases, namespace):
        selectors = {}
        namespace['_item_name'] = name
        namespace['_item_count'] = 0
        for name, value in namespace.items():
            if isinstance(value, Selector):
                selectors[name] = value
        namespace['selectors'] = selectors
        for name in selectors:
            del namespace[name]
        if bases:
            new_objects = list(bases)
            new_objects.append(LogMixin)
            bases = tuple(new_objects)
        return type.__new__(mcs, name, bases, namespace)

    @property
    def name(self):
        return self._item_name

    @property
    def count(self):
        return self._item_count


class Item(metaclass=ItemType):
    def __init__(self, html):
        self.results = {}
        for name, selector in self.selectors.items():
            value = selector.parse_detail(unescape(html))
            if value is None:
                self.error(
                    f'Selector "{selector.rule}" for {name} was wrong, please check again')
            else:
                self.results[name] = value
        if hasattr(self, 'save_url'):
            self.url = getattr(self, 'save_url')
        else:
            self.url = "file:///tmp.data"

    @classmethod
    def count_add(cls, value=1):
        cls._item_count += value

    def __getattr__(self, item):
        if item not in self.results:
            raise AttributeError
        return self.results[item]

    async def save(self):
        if hasattr(self, '__result__'):
            await self.__result__.save(self.results)
        else:
            raise NotImplementedError

    def __repr__(self):
        return f'<item {self.results}>'
