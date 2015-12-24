# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals
import json
import os
import re
import gensim
import jieba
import conf
import data
import logger
import util


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

    logger.log.info("module [processing] initialized.")


def _clean_texts():
    """
    清洗文本
    :rtype: __generator
    """
    # 过滤空白字符
    blank_re = re.compile(r"\s+")
    for row in data.pg.get_pos():
        text = blank_re.split(row["description"])
        # 分词
        text_splited = reduce(lambda x, y: x + jieba.lcut(y), text, [])
        # 过滤停用词
        text_filtered = [word for word in text_splited if word not in data.stopwords]
        yield text_filtered


def _save_texts(path):
    """
    保存文本
    :type path: str or unicode
    :rtype: None
    """
    with open(path, "w") as f:
        cnt = 0
        for row in _clean_texts():
            f.write(json.dumps(row, encoding="utf-8") + "\n")

            cnt += 1
            if cnt % 1000 == 0:
                logger.log.info("texts is saving... number: %s." % (cnt,))

    logger.log.info("texts was saved on disk.")


def text_process():
    """
    处理position的文字信息
    :rtype: NoneType
    """
    if not os.path.exists("tmp/pos_data.txt"):
        _save_texts("tmp/pos_data.txt")

    util.topic_model.build_lda()

    logger.log.info("texts was processed.")
