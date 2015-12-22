# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals
from data import pg
import codecs
import nltk

# 加载nltk.corpus.stopwords停用词
english_stopwords = set(nltk.corpus.stopwords.words('english'))
chinese_stopwords = {word[:-1] for word in codecs.open("data/stopwords.txt", "rU", encoding="utf-8")}

stopwords = english_stopwords | chinese_stopwords
