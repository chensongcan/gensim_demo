# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals
import codecs
import copy
import datetime
import json
import operator
import jieba
import conf
import data
import util


def run(index, model, dictionary, raw_pos):
    """
    :type index: gensim.similarities.Similarity
    :type model: gensim.models.LdaMulticore
    :type dictionary: gensim.corpora.Dictionary
    :type raw_pos: list
    :rtype: NoneType
    """
    global _raw_pos
    _raw_pos = raw_pos

    # school_list = data.pg.get_school()
    major_list = json.load(open("data/major.json", "rU"), encoding="utf-8")
    school_list = [
        {"name": "北京航空航天大学", "city": "北京市"}
    ]

    tb_pos = {}
    for ele in raw_pos:
        tb_pos[ele["id"]] = ele

    with codecs.open("data/result.json", "w", encoding="utf-8") as f:
        for major in major_list:
            query = [word for word in jieba.cut_for_search(major) if word not in data.stopwords]
            query_bow = dictionary.doc2bow(query)
            # 映射到主题空间
            query_model = model[query_bow]
            # 计算相似度
            sim_list = index[query_model]

            # 将新的计算结果更新到数据库中
            for school in school_list:
                rec_list = _weight(sim_list, school=school, major=major)[:30]
                rec_json_list = []
                for item in rec_list:
                    ele = copy.deepcopy(tb_pos[item["id"]])
                    ele["value"] = item["value"]
                    ele["publish_date"] = unicode(ele["publish_date"])
                    rec_json_list.append(ele)
                rec_json = {"school": school, "major": major, "recId": rec_json_list}
                f.write(json.dumps(rec_json, ensure_ascii=False, indent=2) + "\n")


def _weight(sim_list, school=None, major=None):
    """
    加权函数
    :type sim_list: list or numpy.ndarray
    :type school: dict or NoneType
    :type major: str or unicode or NoneType
    :rtype: list
    """
    global _raw_pos
    rec_list = []
    for idx, sim in enumerate(sim_list):
        if isinstance(sim, tuple):
            pos = _raw_pos[sim[0]]
            value = sim[1]
        else:
            pos = _raw_pos[idx]
            value = sim

        # 增加企业端的筛选条件
        if (pos.get("school") and school["name"] not in pos["school"]) or (
                    pos.get("major") and major not in pos["major"]):
            continue

        # 急聘职位提高权重
        value *= conf.RECRUIT_VALUE if pos.get("company_id") else 1

        # 同城职位权值提高
        value *= 1.2 if school["city"] == pos["city"] else 1

        # 增加发布时间递减效应
        value *= util.weight_func.half_life(
                (datetime.datetime.utcnow() - pos["publish_date"].replace(tzinfo=None)).days)

        rec_list.append({"id": pos["id"], "value": value})

    rec_list.sort(key=operator.itemgetter("value"), reverse=True)
    return rec_list
