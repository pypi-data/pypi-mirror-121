#!/usr/bin/env python
# coding=utf-8
# @Time    : 2021/1/12 10:31
# @Author  : 江斌
# @Software: PyCharm
import os
from flask import Flask, render_template
from DaoProject.graph import DaoGraph

app = Flask(__name__)

STATIC_ROOT = r'F:\workspace\gitee\technology\python\examples\DaoProject\scripts\render.html'


@app.route("/")
def index():
    with open(STATIC_ROOT, 'r') as f:
        content = f.read()
    return content


@app.route("/graph/<keywords>")
def graph(keywords):
    graph = DaoGraph()
    keyword_list = keywords.split(',')
    graph.run(keywords=keyword_list)
    with open(STATIC_ROOT, 'r') as f:
        content = f.read()
    return content


if __name__ == '__main__':
    app.run(debug=True)
