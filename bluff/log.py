# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     log
   Description :
   date：          6/28/18
-------------------------------------------------
   Change Activity:
                   6/28/18:
-------------------------------------------------
"""

# Python standard library module
import logging
logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s] %(message)s',
                    datefmt='%Y:%m:%d %H:%M:%S')
logger = logging.getLogger('running')
