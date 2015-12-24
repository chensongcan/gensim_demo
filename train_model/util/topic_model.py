# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals
import json
import os
import gensim
import logger


def _get_doc_col():
    """
    :rtype: __generator
    """
    for cnt, row in enumerate(open("tmp/pos_data.txt", "rU")):
        yield json.loads(row[:-1], encoding="utf-8")

        if cnt % 1000 == 0:
            logger.log.info("texts is being read... number: %s." % (cnt,))


def _get_corpus(dictionary):
    """
    :type dictionary: gensim.corpora.Dictionary
    :rtype: __generator
    """
    for text in _get_doc_col():
        yield dictionary.doc2bow(text)


def _build_dictionary(path):
    """
    建立词袋
    :type path: str or unicode
    :rtype: gensim.corpora.Dictionary
    """
    if os.path.exists(path):
        dictionary = gensim.corpora.Dictionary.load(path)
    else:
        dictionary = gensim.corpora.Dictionary(_get_doc_col(), prune_at=None)
        dictionary.save(path)

    logger.log.info("dictionary was saved on disk.")
    return dictionary


def _build_corpus(dictionary, path):
    """
    建立用词频表示的文档向量
    :type dictionary: gensim.corpora.Dictionary
    :type path: str or unicode
    :rtype: gensim.corpora.MmCorpus
    """
    if not os.path.exists(path):
        gensim.corpora.MmCorpus.serialize("tmp/pos_corpus.mm", _get_corpus(dictionary))
    corpus = gensim.corpora.MmCorpus("tmp/pos_corpus.mm")

    logger.log.info("corpus was saved on disk.")
    return corpus


def _build_lda(corpus, path):
    """
    建立LDA模型
    :type corpus: gensim.corpora.MmCorpus
    :type path: str or unicode
    :rtype: gensim.models.LdaMulticore
    """
    # 建立LDA模型
    lda = gensim.models.LdaMulticore(corpus, num_topics=300, passes=30, alpha=50 / 300, eta=0.01)
    lda.save(path)

    logger.log.info("lda model was saved on disk.")
    return lda


def build_lda():
    """
    建立LDA模型
    :rtype: NoneType
    """
    logger.log.info("model start generating...")

    dictionary = _build_dictionary("tmp/position.dict")
    corpus = _build_corpus(dictionary, "tmp/pos_corpus.mm")
    _build_lda(corpus, "tmp/lda.model")

    logger.log.info("model was generated.")
