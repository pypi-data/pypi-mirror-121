# !/usr/bin/python
# -*- coding: utf-8 -*-
# @time    : 2021/8/29 21:11
# @author  : Mo
# @function: transform conll to span, 将CONLL格式的数据转化为SPAN格式{pos:[1,3]}


import logging


def txt_write(lines, path: str, model: str = "w", encoding: str = "utf-8"):
    """
    Write Line of list to file
    Args:
        lines: lines of list<str> which need save
        path: path of save file, such as "txt"
        model: type of write, such as "w", "a+"
        encoding: type of encoding, such as "utf-8", "gbk"
    """

    try:
        file = open(path, model, encoding=encoding)
        file.writelines(lines)
        file.close()
    except Exception as e:
        logging.info(str(e))
def save_json(lines, path, encoding: str = "utf-8", indent: int = 4):
    """
    Write Line of List<json> to file
    Args:
        lines: lines of list[str] which need save
        path: path of save file, such as "json.txt"
        encoding: type of encoding, such as "utf-8", "gbk"
    """

    with open(path, "w", encoding=encoding) as fj:
        fj.write(json.dumps(lines, ensure_ascii=False, indent=indent))
    fj.close()
def read_corpus(corpus_path):
    """读取CONLL数据
    read corpus for sequence-labeling
    Args:
        corpus_path: String, path/origin text,  eg. "ner.conll"
    Returns:
        data: List<tuple>, <sent_, tag_>
    """
    xs, ys = [], []
    with open(corpus_path, encoding="utf-8") as fr:
        for line in fr:
            line_json = json.loads(line)
            xs.append((line_json.get("sentence", ""), line_json.get("label_desc", "")))
            ys.append(line_json.get("label_desc", ""))

    return xs, ys


if __name__ == '__main__':
    import json
    import sys
    import os
    path_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    sys.path.append(path_root)
    print(path_root)
    path = path_root + "/corpus/text_classification/org_tnews/"
    for t in ["train", "dev", "test"]:
        t = t + ".json"
        xs, ys = read_corpus(path + t)
        res = []
        for d in xs:
            line = {"label":d[1], "text":d[0]}
            res.append(json.dumps(line, ensure_ascii=False) + "\n")
        txt_write(res, path + t + ".span")

        ee = 0
    # transform conll to span, 将CONLL格式的数据转化为SPAN格式{pos:[1,3]}


