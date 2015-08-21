# 中文Wiki的Word2Vec测试

全部流程参照[用mecab打造一套实用的中文分词系统](http://www.52nlp.cn/用mecab打造一套实用的中文分词系统)一文。

```shell
python process_wiki.py data/zhwiki-latest-pages-articles.xml.bz2 wiki.zh.txt

opencc -i wiki.zh.txt -o wiki.zh_cn.txt -c t2s.json

mecab -d mecab-chinesedic-binary/ -O wakati wiki.zh_cn.txt -o wiki.zh_cn.seg.txt -b 10000000

iconv -c -t UTF-8 < wiki.zh_cn.seg.txt > wiki.zh_cn.seg.utf-8.txt

python train_word2vec_model.py wiki.zh_cn.seg.utf-8.txt model/wiki.zh_cn.model model/wiki.zh_cn.vector
```

[gensim](http://radimrehurek.com/gensim/)是一个Python上比较流行的文本处理库，实现了LSI、LDA等主题模型，以及[Word2Vec](https://code.google.com/p/word2vec/)等模型，依赖于Numpy、Scipy，常常与NLTK搭配使用。

该测试采用语料为[中文Wiki Dump](http://download.wikipedia.com/zhwiki/latest/zhwiki-latest-pages-articles.xml.bz2)。

[MeCab](http://taku910.github.io/mecab/)是一个在日本NLP界广泛采用的基于CRF的日文分词系统，提供中文词典和数据模型后可用于中文分词。中文词典和数据模型采用了文中作者自制的mecab-chinesesdic-binary（链接：[http://pan.baidu.com/s/1gdxnvFX](http://pan.baidu.com/s/1gdxnvFX)，密码：kq9g），经[Bakeoff 2005](http://sighan.cs.uchicago.edu/bakeoff2005/)的icwb2-data中的PKU和MSR分词测试集测试，分词效果优于[jieba分词](https://github.com/fxsjy/jieba)。

[opencc](https://github.com/BYVoid/OpenCC)是一个由BYVoid等人支持的中文简繁转换开源项目。

iconv是一个常见的编码转换工具，调用了[libiconv库](http://www.gnu.org/software/libiconv/)。
