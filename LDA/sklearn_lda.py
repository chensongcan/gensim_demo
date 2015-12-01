# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
import operator
import sklearn.decomposition
import sklearn.feature_extraction.text
import sklearn.metrics.pairwise

try:
    import preprocess
except ImportError:
    from LDA import preprocess

courses_name = preprocess.courses_name
query_idx = 210
texts = preprocess.texts
texts = map(lambda text: " ".join(text), texts)


def build_nmf():
    global query, sims
    vectorizer = sklearn.feature_extraction.text.TfidfVectorizer()
    corpus_tfidf = vectorizer.fit_transform(texts)

    nmf = sklearn.decomposition.NMF(n_components=20, verbose=1)
    corpus = nmf.fit_transform(corpus_tfidf)
    index = sklearn.metrics.pairwise.cosine_distances(corpus)
    print index
    query = corpus[query_idx]
    sims = index[query_idx]


def build_lda():
    global query, sims
    vectorizer = sklearn.feature_extraction.text.CountVectorizer()
    corpus_tf = vectorizer.fit_transform(texts)

    lda = sklearn.decomposition.LatentDirichletAllocation(n_topics=20, learning_method="online", max_iter=50,
                                                          evaluate_every=10, verbose=1)
    corpus = lda.fit_transform(corpus_tf)
    print lda.perplexity(corpus_tf)
    index = sklearn.metrics.pairwise.cosine_distances(corpus)
    query = corpus[query_idx]
    sims = index[query_idx]


def output():
    print courses_name[query_idx], query
    sort_sims = sorted(enumerate(sims), key=operator.itemgetter(1), reverse=True)
    for idx in sort_sims[:10]:
        print courses_name[idx[0]], idx


# build_nmf()
build_lda()
output()
