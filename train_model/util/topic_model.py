# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals
import gensim
import logger

dictionary = None
corpus = None
model = None


def _build_corpus(doc_col):
    """
    建立词袋和文档向量
    :param doc_col:
    :return:
    """
    global dictionary, corpus
    # 抽取词袋
    dictionary = gensim.corpora.Dictionary(doc_col)
    dictionary.save("position.dict")
    # 建立用词频表示的文档向量
    corpus = [dictionary.doc2bow(text) for text in doc_col]
    gensim.corpora.MmCorpus.serialize("pos_corpus.mm", corpus)


def _build_lda():
    """
    建立LDA模型
    :return:
    """
    global index
    # 建立LDA模型
    lda = gensim.models.LdaMulticore(corpus, id2word=dictionary, num_topics=300, passes=200, alpha=50 / 300, eta=0.01)
    lda.save("lda.model")
    return lda


def build_lda(doc_col):
    """
    建立LDA模型
    :param doc_col:
    :return:
    """
    global model
    _build_corpus(doc_col)
    model = _build_lda()
    logger.log.info("lda model was generated.")
