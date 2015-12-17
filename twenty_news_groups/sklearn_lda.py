# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
import sklearn.decomposition
import sklearn.feature_extraction.text

try:
    import preprocess
except ImportError:
    from twenty_news_groups import preprocess


def print_top_words(model, feature_names):
    for topic_idx, topic in enumerate(model.components_):
        print "Topic #%d:" % topic_idx
        print " ".join([feature_names[i] for i in topic.argsort()[:-20 - 1:-1]])


def build_nmf():
    tfidf_vectorizer = sklearn.feature_extraction.text.TfidfVectorizer(max_df=0.95, min_df=2, stop_words='english')
    tfidf = tfidf_vectorizer.fit_transform(preprocess.data)

    nmf = sklearn.decomposition.NMF(n_components=10, random_state=1, alpha=0.1, l1_ratio=0.5)
    nmf.fit(tfidf)

    tfidf_feature_names = tfidf_vectorizer.get_feature_names()
    print_top_words(nmf, tfidf_feature_names)


def build_lda():
    tf_vectorizer = sklearn.feature_extraction.text.CountVectorizer(max_df=0.95, min_df=2, stop_words='english')
    tf = tf_vectorizer.fit_transform(preprocess.data)

    lda = sklearn.decomposition.LatentDirichletAllocation(n_topics=10, max_iter=5, learning_method='online',
                                                          learning_offset=50, random_state=0)
    lda.fit(tf)

    tf_feature_names = tf_vectorizer.get_feature_names()
    print_top_words(lda, tf_feature_names)


# build_nmf()
build_lda()
