# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     abstract
   Description :
   date：          7/9/18
-------------------------------------------------
   Change Activity:
                   7/9/18:
-------------------------------------------------
"""
# Python standard library module
from abc import ABCMeta, abstractmethod


class Selector(metaclass=ABCMeta):
    def __init__(self, rule, attr=None):
        self.rule = rule
        self.attr = attr

    def __str__(self):
        return f'{self.__class__.__name__}({self.rule})'

    def __repr__(self):
        return f'{self.__class__.__name__}({self.rule})'

    @abstractmethod
    def parse_detail(self, html):
        raise NotImplementedError
