# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals
import logging

# 脚本日志设置
logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s:%(msecs)05.1f pid:%(process)d [%(levelname)s] (%(funcName)s) %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        filename='train_model.log',
        filemode='a+')

logger = logging.getLogger()
