# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals
import os
import jieba


def init(parallel=False):
    """
    jieba分词初始化
    :param parallel: jieba分词是否并行运行
    :return:
    """
    # 设置结巴分词log级别
    jieba.setLogLevel("INFO")
    # 设置结巴分词字典文件
    jieba.set_dictionary("data/jieba_dict.txt")
    # 修改结巴分词临时工作目录
    jieba.tmp_dir = os.getcwd()
    # 开启并行分词模式，进程数为CPU核心数
    if parallel:
        jieba.enable_parallel()
