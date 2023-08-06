#!/usr/bin/env python
# coding=utf-8
# @Time    : 2021/1/13 11:34
# @Author  : 江斌
# @Software: PyCharm
from DaoProject.server import app


def run():
    app.run(debug=True)


if __name__ == '__main__':
    run()
