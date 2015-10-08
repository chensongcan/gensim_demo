# -*- coding: utf-8 -*-

import logging
import operator

import nltk
import gensim

logging.basicConfig(format="%(asctime)s : %(levelname)s : %(message)s", level=logging.INFO)

query_idx = 210

# 加载数据
courses = [line.strip() for line in file('coursera_corpus')]
courses_name = [course.split('\t')[0] for course in courses]

# 转为小写，根据空格分词
texts_lower = [[word for word in document.lower().split()] for document in courses]

# 使用nltk.tokenize做进一步分词
texts_tokenized = [[word.lower() for word in nltk.tokenize.word_tokenize(document.decode('utf-8'))] for document in
                   courses]

# 加载nltk.corpus.stopwords停用词
english_stopwords = nltk.corpus.stopwords.words('english')

# 过滤停用词
texts_filtered_stopwords = [[word for word in document if word not in english_stopwords] for document in
                            texts_tokenized]

# 过滤标点符号
english_punctuations = [',', '.', ':', ';', '?', '(', ')', '[', ']', '&', '!', '*', '@', '#', '$', '%']
texts_filtered = [[word for word in document if word not in english_punctuations] for document in
                  texts_filtered_stopwords]

# 单词词干化
st = nltk.stem.SnowballStemmer(language="english")
texts_stemmed = [[st.stem(word) for word in document] for document in texts_filtered]

# 过滤低频词
all_stems = sum(texts_stemmed, [])
stems_once = {stem for stem in set(all_stems) if all_stems.count(stem) == 1}
texts = [[stem for stem in text if stem not in stems_once] for text in texts_stemmed]

# 抽取词袋
dictionary = gensim.corpora.Dictionary(texts)

# 建立用词频表示的文档向量
corpus = [dictionary.doc2bow(text) for text in texts]

# 建立TF-IDF模型
tfidf = gensim.models.TfidfModel(corpus)

# 建立用TF-IDF值表示的文档向量
corpus_tfidf = tfidf[corpus]

# 建立LSI模型
lsi = gensim.models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=10)

# 建立相似度索引
index = gensim.similarities.MatrixSimilarity(lsi[corpus])
# index = gensim.similarities.Similarity("lsiIndex", lsi[corpus], num_features=lsi.num_topics, num_best=10)

query_lsi = lsi[corpus[query_idx]]
# query = texts[query_idx]
# # 查询向量化
# query_bow = dictionary.doc2bow(query)
# # 映射到主题空间
# query_lsi = lsi[query_bow]
# 计算相似度
sims = index[query_lsi]

# # 建立LDA模型
# lda = gensim.models.LdaModel(corpus, id2word=dictionary, num_topics=50, passes=10)
#
# # 建立相似度索引
# index = gensim.similarities.MatrixSimilarity(lda[corpus])
#
# query = texts[query_idx]
# # 查询向量化
# query_bow = dictionary.doc2bow(query)
# # 映射到主题空间
# query_lda = lda[query_bow]
# # 计算相似度
# sims = index[query_lda]

# # 建立HDP模型
# hdp = gensim.models.HdpModel(corpus, id2word=dictionary)
#
# # 建立相似度索引
# index = gensim.similarities.MatrixSimilarity(hdp[corpus])
#
# query = texts[query_idx]
# # 查询向量化
# query_bow = dictionary.doc2bow(query)
# # 映射到主题空间
# query_hdp = hdp[query_bow]
# # 计算相似度
# sims = index[query_hdp]

print courses_name[query_idx], query_lsi
sort_sims = sorted(enumerate(sims), key=operator.itemgetter(1), reverse=True)
for idx in sort_sims[:10]:
    print courses_name[idx[0]], idx
# for idx in sims:
#     print courses_name[idx[0]], idx
