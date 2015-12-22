# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals
import json
import gensim
import logger

dictionary = None
corpus = None
model = None


def _get_doc_col():
    """
    :return:
    """
    for row in open("pos_data.txt", "r"):
        yield json.loads(row[:-1], encoding="utf-8")


def _get_corpus():
    """
    :return:
    """
    for text in _get_doc_col():
        yield dictionary.doc2bow(text)


def _build_corpus():
    """
    建立词袋和文档向量
    :return:
    """
    global dictionary, corpus
    # 抽取词袋
    dictionary = gensim.corpora.Dictionary(_get_doc_col(), prune_at=None)
    dictionary.save("position.dict")

    # 建立用词频表示的文档向量
    gensim.corpora.MmCorpus.serialize("pos_corpus.mm", _get_corpus)
    corpus = gensim.corpora.MmCorpus("pos_corpus.mm")


def _build_lda():
    """
    建立LDA模型
    :return:
    """
    # 建立LDA模型
    lda = gensim.models.LdaMulticore(corpus, id2word=dictionary, num_topics=300, passes=200, alpha=50 / 300, eta=0.01)
    lda.save("lda.model")
    return lda


def build_lda():
    """
    建立LDA模型
    :return:
    """
    global model
    _build_corpus()
    model = _build_lda()
    logger.log.info("lda model was generated.")
