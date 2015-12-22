# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals
import copy
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


def text_process(pos):
    """
    处理position的文字信息
    :param pos:
    :return:
    """
    contents = _clean_content(pos)
    util.topic_model.build_lda(contents)

    logger.log.info("text was processed.")


def _clean_content(raw):
    """
    文本清洗
    :param raw:
    :return:
    """
    # 过滤空白字符
    blank_re = re.compile(r"\s+")
    texts_raw = [blank_re.split(ele["description"]) for ele in raw]

    # 分词
    texts_splited = [reduce(lambda x, y: x + jieba.lcut(y), text, []) for text in texts_raw]

    # 过滤停用词
    texts_filtered = [[word for word in text if word not in data.stopwords] for text in texts_splited]

    # 过滤低频词
    # all_words = sum(texts_filtered, [])
    # words_once = {word for word in set(all_words) if all_words.count(word) == 1}
    # texts = [[word for word in text if word not in words_once] for text in texts_filtered]

    logger.log.info("text was cleaned.")
    return texts_filtered
