# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals
import conf


def half_life(t):
    """
    时间递减函数
    :param t:
    :type t: float
    :return:
    :rtype: float
    """
    return 0.5 ** ((t - 14) / conf.HALF_TIME_INTERVAL) if t > 14 else 1
