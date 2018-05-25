# -*- coding: UTF-8 -*-
#!flask/bin/python
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, Response
from gensim import corpora, similarities, models
import jieba
import json
import configparser
import sqlalchemy_jsonfield

app = Flask(__name__)

my_config = configparser.ConfigParser()
my_config.read('db.conf')

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://' + my_config.get('DB', 'DB_USER') + ':' + my_config.get(
    'DB', 'DB_PASSWORD') + '@' + my_config.get('DB', 'DB_HOST') + '/' + my_config.get('DB', 'DB_DB')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class Mapping(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mapping = db.Column(
        sqlalchemy_jsonfield.JSONField(
            enforce_string=True,
            enforce_unicode=False
        ),
        nullable=False
    )

    def __init__(self, id, mapping):
        self.id = id
        self.mapping = mapping


def remove_stopwords(word_list, stopwords):
    cleaned_word_list = []
    for word in word_list:
        if word not in stopwords:
            cleaned_word_list.append(word)
    return cleaned_word_list


@app.route('/',  methods=['POST'])
def index():
    requestJson = request.get_json(force=True)
    if requestJson["content"] == "":
        return Response(json.dumps({"error_code": "4000", "msg": "内容不能为空"}), mimetype='application/json')

    proposal = requestJson["content"].replace(' ', '').replace(
        '\t', '').replace('\r\n', '').replace('\r', '').replace('\n', '')

    stopwords = set([line.strip()
                     for line in open('dict/stopword.dic').readlines()])

    dictionary = corpora.Dictionary.load("dict/dict.txt")
    #tfidf = models.TfidfModel.load("dict/data.tfidf")
    corpus = corpora.MmCorpus('dict/corpuse.mm')

    tfidf_model = models.TfidfModel(corpus)
    corpus_tfidf = tfidf_model[corpus]

    lsi = models.LsiModel(corpus_tfidf, num_topics=100)
    corpus_lsi = lsi[corpus_tfidf]
    similarity_lsi = similarities.Similarity(
        'dict/Similarity-LSI-index', corpus_lsi, num_features=100, num_best=20)

    test_cut_raw_3 = list(jieba.cut(proposal))         # 1.分词
    cleaned_words_list3 = remove_stopwords(test_cut_raw_3, stopwords)
    test_corpus_3 = dictionary.doc2bow(cleaned_words_list3)  # 2.转换成bow向量
    test_corpus_tfidf_3 = tfidf_model[test_corpus_3]  # 3.计算tfidf值
    test_corpus_lsi_3 = lsi[test_corpus_tfidf_3]  # 4.计算lsi值
    # lsi.add_documents(test_corpus_lsi_3) #更新LSI的值
    result = similarity_lsi[test_corpus_lsi_3]

    nlp_result = []
    mapList = Mapping.query.order_by(Mapping.id.desc()).first()
    for r in result:
        nlp_result.append({"id": mapList.mapping[r[0]], "ratio": r[1]})

    return Response(json.dumps(nlp_result), mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=True)
