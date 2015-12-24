# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals
import json
import os
import gensim
import logger


def _get_doc_col(path):
    """
    :type path: str or unicode
    :rtype: __generator
    """
    for cnt, row in enumerate(open(path, "rU")):
        yield json.loads(row[:-1], encoding="utf-8")
        if cnt % 2000 == 0:
            logger.log.info("texts is being read... number: %s." % (cnt,))


def _get_corpus(dictionary, path):
    """
    :type dictionary: gensim.corpora.Dictionary
    :type path: str or unicode
    :rtype: __generator
    """
    for text in _get_doc_col(path):
        yield dictionary.doc2bow(text)


def build_dictionary(data, path=None):
    """
    建立词袋
    :type data: str or unicode
    :type path: str or unicode or None
    :rtype: gensim.corpora.Dictionary
    """
    if path and os.path.exists(path):
        dictionary = gensim.corpora.Dictionary.load(path)
        logger.log.info("dictionary was loaded from disk.")
    else:
        dictionary = gensim.corpora.Dictionary(_get_doc_col(data), prune_at=None)
        if path:
            dictionary.save(path)
            logger.log.info("dictionary was saved on disk.")
    logger.log.info("dictionary was generated.")
    return dictionary


def _build_corpus(dictionary, data, path=None):
    """
    建立用词频表示的文档向量
    :type dictionary: gensim.corpora.Dictionary
    :type data: str or unicode
    :type path: str or unicode or None
    :rtype: gensim.corpora.MmCorpus
    """
    if path and os.path.exists(path):
        corpus = gensim.corpora.MmCorpus(path)
        logger.log.info("corpus was loaded from disk.")
    else:
        corpus = _get_corpus(dictionary, data)
        if path:
            gensim.corpora.MmCorpus.serialize(path, corpus)
            logger.log.info("corpus was saved on disk.")
    return corpus


def build_lda(dictionary):
    """
    建立LDA模型
    :type dictionary: gensim.corpora.Dictionary
    :rtype: gensim.models.LdaMulticore
    """
    corpus = _build_corpus(dictionary, data="tmp/pos_data.txt", path="tmp/pos_corpus.mm")
    model = gensim.models.LdaMulticore(corpus, id2word=dictionary, num_topics=300, passes=50, alpha=50 / 300, eta=0.01)
    model.save("tmp/lda.model")
    logger.log.info("lda model was saved on disk.")
    logger.log.info("lda model was generated.")
    return model


def build_index(model, dictionary):
    """
    建立相似文档索引
    :type model: gensim.models.LdaMulticore
    :type dictionary: gensim.corpora.Dictionary
    :rtype: gensim.similarities.Similarity
    """
    corpus = _build_corpus(dictionary, data="tmp/pos_index.txt")
    index = gensim.similarities.Similarity("lda.index", model[corpus], num_features=model.num_topics)
    logger.log.info("index was generated.")
    return index
