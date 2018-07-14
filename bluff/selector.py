# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     selector
   Description :
   date：          6/28/18
-------------------------------------------------
   Change Activity:
                   6/28/18:
-------------------------------------------------
"""
# Python standard library module
import re
from abc import ABCMeta, abstractmethod
# Python third party module
from lxml import etree
from pyquery import PyQuery as pq
# Application custom module


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


class Css(Selector):
    def parse_detail(self, html):
        dom = pq(html)
        if self.attr is None:
            try:
                return dom(self.rule)[0].text
            except IndexError as e:
                return None
        return dom(self.rule)[0].attr(self.attr, None)


class Xpath(Selector):
    def parse_detail(self, html):
        dom = etree.HTML(html)
        try:
            if self.attr is None:
                if len(dom.xpath(self.rule)) > 1:
                    return [entry.text for entry in dom.xpath(self.rule)]
                else:
                    return dom.xpath(self.rule)[0].text
            return [
                entry.get(
                    self.attr,
                    None) for entry in dom.xpath(
                    self.rule)] if len(
                dom.xpath(
                    self.rule)) > 1 else dom.xpath(
                        self.rule)[0].text
        except IndexError as e:
            return None


class Regex(Selector):
    def parse_detail(self, html):
        try:
            return re.findall(self.rule, html)[0]
        except IndexError as e:
            return None
