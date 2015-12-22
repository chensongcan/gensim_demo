# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals
import json
import re
import gensim
import jieba
import conf
import data
import logger
import util


def init(jieba_parallel=False):
    """
    配置中文分词设置
    :param jieba_parallel: jieba分词是否并行运行
    :return:
    """
    conf.jieba.init(jieba_parallel)

    gensim.logger.setLevel("WARNING")

    logger.log.info("module [preprocess] initialized.")


def text_process():
    """
    处理position的文字信息
    :return:
    """
    with open("pos_data.txt", "w") as f:
        for row in _clean_content():
            f.write(json.dumps(row, encoding="utf-8") + "\n")

    util.topic_model.build_lda()

    logger.log.info("text was processed.")


def _clean_content():
    """
    文本清洗
    :return:
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
