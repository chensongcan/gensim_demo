# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
import operator
import gensim

try:
    import preprocess
except ImportError:
    from LDA import preprocess

courses_name = preprocess.courses_name
query_idx = 210
texts = preprocess.texts

# 抽取词袋
dictionary = gensim.corpora.Dictionary(texts)

# 建立用词频表示的文档向量
corpus = [dictionary.doc2bow(text) for text in texts]


def build_lsi():
    """建立LSI模型"""
    global query, sims
    tfidf = gensim.models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]

    lsi = gensim.models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=20)
    index = gensim.similarities.MatrixSimilarity(lsi[corpus])
    query = lsi[corpus[query_idx]]
    sims = index[query]


def build_lda():
    """建立LDA模型"""
    global query, sims
    lda = gensim.models.LdaModel(corpus, id2word=dictionary, num_topics=100, passes=100, alpha=50 / 100, eta=0.01)
    index = gensim.similarities.MatrixSimilarity(lda[corpus])
    query = lda[corpus[query_idx]]
    sims = index[query]


def build_hdp():
    """建立HDP模型"""
    global query, sims
    hdp = gensim.models.HdpModel(corpus, id2word=dictionary)
    index = gensim.similarities.MatrixSimilarity(hdp[corpus])
    query = hdp[corpus[query_idx]]
    sims = index[query]


def output():
    print courses_name[query_idx], query
    sort_sims = sorted(enumerate(sims), key=operator.itemgetter(1), reverse=True)
    for idx in sort_sims[:10]:
        print courses_name[idx[0]], idx


# build_lsi()
build_lda()
# build_hdp()
output()
