# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals
import codecs
import json
import os
import re
import gensim
import jieba
import conf
import data
import logger


def init(jieba_parallel=False, gensim_warning=False):
    """
    初始化
    :type jieba_parallel: bool
    :type gensim_warning: bool
    :rtype: NoneType
    """
    conf.jieba.init(jieba_parallel)
    if gensim_warning:
        gensim.logger.setLevel("WARNING")
    logger.log.info("module [text_process] initialized.")


def _clean_texts(pos_list):
    """
    清洗文本
    :type pos_list: list or __generator
    :rtype: __generator
    """
    # 过滤空白字符
    blank_re = re.compile(r"\s+")
    for row in pos_list:
        text = blank_re.split(row["description"])
        # 分词
        text_splited = reduce(lambda x, y: x + jieba.lcut(y), text, [])
        # 过滤停用词
        text_filtered = [word for word in text_splited if word not in data.stopwords]
        yield text_filtered


def _save_texts(path, pos_list):
    """
    保存文本
    :type path: str or unicode
    :type pos_list: list or __generator
    :rtype: None
    """
    with codecs.open(path, "w", encoding="utf-8") as f:
        cnt = 0
        for row in _clean_texts(pos_list):
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
            cnt += 1
            if cnt % 2000 == 0:
                logger.log.info("texts is saving... number: %s." % (cnt,))
    logger.log.info("texts was saved on disk.")


def run(path, pos_list):
    """
    处理position的文字信息
    :type path: str or unicode
    :type pos_list: list or __generator
    :rtype: NoneType
    """
    if not os.path.exists(path):
        _save_texts(path, pos_list)
    logger.log.info("texts was processed.")
