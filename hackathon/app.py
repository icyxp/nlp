# -*- coding: UTF-8 -*-
#!flask/bin/python
from flask import Flask
from gensim import corpora, similarities, models
import jieba
import json
import configparser
import MySQLdb as mdb

app = Flask(__name__)


def remove_stopwords(word_list, stopwords):
    cleaned_word_list = []
    for word in word_list:
        if word not in stopwords:
            cleaned_word_list.append(word)
    return cleaned_word_list


@app.route('/')
def index():
    try:
        config = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'xupeng',
            'passwd': 'xupeng',
            'db': 'heima',
            'charset': 'utf8'
        }
        conn = mdb.connect(**config)
        cursor = conn.cursor()

        cursor.execute(
            "select `mapping` from mapping order by id desc limit 1")
        mapping = cursor.fetchone()
        map_result = json.loads(mapping[0])
    finally:
        cursor.close()
        conn.close()

    stopwords = set([line.strip()
                     for line in open('dict/stopword.dic').readlines()])

    dictionary = corpora.Dictionary.load("dict/dict.txt")
    tfidf = models.TfidfModel.load("dict/data.tfidf")
    corpus = corpora.MmCorpus('dict/corpuse.mm')

    tfidf_model = models.TfidfModel(corpus)
    corpus_tfidf = tfidf_model[corpus]

    lsi = models.LsiModel(corpus_tfidf)
    corpus_lsi = lsi[corpus_tfidf]
    similarity_lsi = similarities.Similarity(
        'dict/Similarity-LSI-index', corpus_lsi, num_features=400, num_best=2)

    test_data_3 = '随着互联网的发展和普及,域名系统作为互联网的重要基础设施,对人们的网络生活有着至关重要的影响。而DNS(域名系统)递归服务器,作为和客户端直接交互的域名服务器,其健康状况和服务质量直接关系到用户获取到的解析数据的完整性、正确性和及时性。因此,如何为用户推荐健康状况好、服务质量优的DNS递归服务器成为如今网络安全领域中亟待解决的问题。本文通过探测获取DNS递归服务器基础信息和服务质量,提出了DNS递归服务器健康状况评估模型和服务质量评估模型,并设计实现了DNS递归服务器推荐系统,为用户推荐适合的、健康状况好、服务质量优的DNS递归服务器。首先,本文介绍了DNS相关理论,包括DNS基础理论、DNS信息探测的相关理论和方法以及DNS评价与推荐的相关理论和方法。其次,本文设计并实现了DNS递归服务器推荐系统。该系统分为数据探测、数据分析和推荐评价三个模块。其中数据探测包括DNS递归服务器基础信息探测和服务质量探测,探测了DNS类型、协议支持情况、软件版本信息、漏洞信息等基础信息,以及网络性能和DNS可解析性等服务质量。数据分析包括DNS递归服务器健康状况评估和服务质量评估,分别采用层次分析法和复相关系数法,对基础信息探测结果和服务质量探测结果进行了分析,得到了DNS递归服务器健康状况评估值和服务质量评估值。推荐评价包括综合推荐和当前服务器评价,根据健康状况评估结果和服务质量评估结果,向用户推荐适合的、健康状况好、服务质量优的DNS递归服务器,同时可以对用户当前DNS服务器进行评价。最后,本文测试了DNS递归服务器推荐系统,从功能和性能两个方面对系统的每个模块及其子模块进行了测试。综上所述,本文完成了DNS递归服务器推荐系统。通过系统测试表明,该系统满足设计目标。'
    test_cut_raw_3 = list(jieba.cut(test_data_3))         # 1.分词
    cleaned_words_list3 = remove_stopwords(test_cut_raw_3, stopwords)
    test_corpus_3 = dictionary.doc2bow(cleaned_words_list3)  # 2.转换成bow向量
    test_corpus_tfidf_3 = tfidf_model[test_corpus_3]  # 3.计算tfidf值
    test_corpus_lsi_3 = lsi[test_corpus_tfidf_3]  # 4.计算lsi值
    # lsi.add_documents(test_corpus_lsi_3) #更新LSI的值
    result = similarity_lsi[test_corpus_lsi_3]
    nlp_result = []
    for r in result:
        nlp_result.append({"id": map_result[r[0]], "ratio": r[1]})

    nlp = json.dumps(nlp_result)
    return nlp


if __name__ == '__main__':
    app.run(debug=True)
