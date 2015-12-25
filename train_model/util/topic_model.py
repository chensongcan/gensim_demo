# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals
import json
import os
import gensim
import logger


def get_doc(source):
    """
    :type source: str or unicode
    :rtype: __generator
    """
    cnt = 0
    for row in open(source, "rU"):
        yield json.loads(row[:-1], encoding="utf-8")
        cnt += 1
        if cnt % 2000 == 0:
            logger.log.info("texts is being read... number: %s." % (cnt,))


def _get_corpus(dictionary, source):
    """
    :type dictionary: gensim.corpora.Dictionary
    :type source: str or unicode
    :rtype: __generator
    """
    for text in get_doc(source):
        yield dictionary.doc2bow(text)


def build_dictionary(source, path=None):
    """
    建立词袋
    :type source: str or unicode
    :type path: str or unicode or None
    :rtype: gensim.corpora.Dictionary
    """
    if path and os.path.exists(path):
        dictionary = gensim.corpora.Dictionary.load(path)
        logger.log.info("dictionary was loaded from disk.")
    else:
        dictionary = gensim.corpora.Dictionary(get_doc(source), prune_at=None)
        if path:
            dictionary.save(path)
            logger.log.info("dictionary was saved on disk.")
            dictionary = gensim.corpora.Dictionary.load(path)
    logger.log.info("dictionary was generated.")
    return dictionary


def _build_corpus(dictionary, source, path=None):
    """
    建立用词频表示的文档向量
    :type dictionary: gensim.corpora.Dictionary
    :type source: str or unicode
    :type path: str or unicode or None
    :rtype: __generator or gensim.corpora.MmCorpus
    """
    if path and os.path.exists(path):
        corpus = gensim.corpora.MmCorpus(path)
        logger.log.info("corpus was loaded from disk.")
    else:
        corpus = _get_corpus(dictionary, source)
        if path:
            gensim.corpora.MmCorpus.serialize(path, corpus)
            logger.log.info("corpus was saved on disk.")
            corpus = gensim.corpora.MmCorpus(path)
    return corpus


def build_lda(dictionary, path=None):
    """
    建立LDA模型
    :type dictionary: gensim.corpora.Dictionary
    :type path: str or unicode or None
    :rtype: gensim.models.LdaMulticore or gensim.models.LdaModel
    """
    if path and os.path.exists(path):
        model = gensim.models.LdaMulticore.load(path)
        logger.log.info("lda model was loaded from disk.")
    else:
        corpus = _build_corpus(dictionary, source="tmp/pos_data.txt", path="tmp/pos_corpus.mm")
        model = gensim.models.LdaMulticore(corpus, id2word=dictionary, num_topics=300, passes=30, alpha=50 / 300,
                                           eta=0.01)
        if path:
            model.save(path)
            logger.log.info("lda model was saved on disk.")
            model = gensim.models.LdaMulticore.load(path)
    logger.log.info("lda model was generated.")
    return model


def build_index(model, dictionary, path=None):
    """
    建立相似文档索引
    :type model: gensim.models.LdaMulticore
    :type dictionary: gensim.corpora.Dictionary
    :type path: str or unicode or None
    :rtype: gensim.similarities.Similarity
    """
    if path and os.path.exists(path):
        index = gensim.similarities.Similarity.load(path)
        logger.log.info("index was loaded from disk.")
    else:
        corpus = _build_corpus(dictionary, source="tmp/pos_index.txt")
        index = gensim.similarities.Similarity("pos_index", model[corpus], num_features=model.num_topics)
        if path:
            index.save(path)
            logger.log.info("index was saved on disk.")
            index = gensim.similarities.Similarity.load(path)
    logger.log.info("index was generated.")
    return index
