# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     mixin
   Description :
   date：          7/9/18
-------------------------------------------------
   Change Activity:
                   7/9/18:
-------------------------------------------------
"""

# Application custom module
from .log import logger


class LoggerMixin:
    @classmethod
    def info(cls, msg):
        logger.info(msg)

    @classmethod
    def error(cls, msg):
        logger.error(msg)

