# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals
import json
import gensim
import logger


def _get_doc_col():
    """
    :rtype: generator
    """
    cnt = 0
    for row in open("pos_data.txt", "r"):
        yield json.loads(row[:-1], encoding="utf-8")
        cnt += 1
        if cnt % 1000 == 0:
            logger.log.info("texts is being read... number: %s." % (cnt,))


def _get_corpus(dictionary):
    """
    :rtype: generator
    """
    cnt = 0
    for text in _get_doc_col():
        yield dictionary.doc2bow(text)
        cnt += 1
        if cnt % 1000 == 0:
            logger.log.info("corpus is saving... number: %s." % (cnt,))


def _build_dictionary():
    """
    建立词袋
    :rtype: gensim.corpora.Dictionary
    """
    dictionary = gensim.corpora.Dictionary(_get_doc_col(), prune_at=None)
    dictionary.save("position.dict")

    logger.log.info("dictionary was saved on disk.")
    return dictionary


def _build_corpus(dictionary):
    """
    建立用词频表示的文档向量
    :type dictionary: gensim.corpora.Dictionary
    :rtype: gensim.corpora.MmCorpus
    """
    gensim.corpora.MmCorpus.serialize("pos_corpus.mm", _get_corpus(dictionary))
    corpus = gensim.corpora.MmCorpus("pos_corpus.mm")

    logger.log.info("corpus was saved on disk.")
    return corpus


def _build_lda(corpus):
    """
    建立LDA模型
    :type corpus: gensim.corpora.MmCorpus
    :rtype: gensim.models.LdaMulticore
    """
    # 建立LDA模型
    lda = gensim.models.LdaMulticore(corpus, num_topics=300, passes=200, alpha=50 / 300, eta=0.01)
    lda.save("lda.model")
    logger.log.info("lda model was saved on disk.")
    return lda


def build_lda():
    """
    建立LDA模型
    :rtype: NoneType
    """
    logger.log.info("model start generating...")

    dictionary = _build_dictionary()
    corpus = _build_corpus(dictionary)
    _build_lda(corpus)

    logger.log.info("model was generated.")
