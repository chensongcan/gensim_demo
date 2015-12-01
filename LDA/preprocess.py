# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
import logging
import re
import nltk

logging.basicConfig(format="%(asctime)s : %(levelname)s : %(message)s", level=logging.INFO)

# 加载数据
courses = [line.strip() for line in file("coursera_corpus")]
courses_name = [course.split("\t")[0] for course in courses]

# 剔除标点符号
texts = map(lambda text: re.sub(r"[^A-Za-z]+", " ", text), courses)

# 使用nltk.tokenize.word_tokenize分词
texts = map(lambda text: [word.lower() for word in nltk.tokenize.word_tokenize(text)], texts)

# 过滤nltk.corpus.stopwords停用词
texts = map(lambda text: [word for word in text if word not in nltk.corpus.stopwords.words("english")], texts)

# 使用nltk.stem.WordNetLemmatizer单词词干化
texts = map(lambda text: [nltk.stem.WordNetLemmatizer().lemmatize(word) for word in text], texts)
# texts = map(lambda text: [nltk.stem.SnowballStemmer(language="english").stem(word) for word in text], texts)

# # 过滤低频词
# all_stems = sum(texts, [])
# stems_once = {stem for stem in set(all_stems) if all_stems.count(stem) == 1}
# texts = map(lambda text: [stem for stem in text if stem not in stems_once], texts)
