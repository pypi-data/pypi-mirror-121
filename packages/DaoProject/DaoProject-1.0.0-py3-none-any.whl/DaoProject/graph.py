#!/usr/bin/env python
# coding=utf-8
# @Time    : 2021/1/11 17:01
# @Author  : 江斌
# @Software: PyCharm

from pyecharts import options as opts
from pyecharts.charts import Graph, Page
from DaoProject.contents import Daos, DaoContent


class DaoGraph(object):
    def __init__(self):
        self.dao = DaoContent()
        self.relations = None
        self.nodes = None
        self.links = None

    def init_relations(self, keywords=None):
        if keywords is None:
            keywords = ['道', '一', '中', '知', '象', '有', '无', '天之道', '柔', '马', '水', '无为', '谷', '下', '雌', '静', '善',
                        '去彼取此']
        relations = [(k, self.dao.get_index_by_word(k)) for k in keywords]
        return relations

    def get_node_list(self):
        nodes = [
            {"name": item,
             "symbolSize": 20,
             "value": Daos[item],
             "label": {"formatter": f'{item}:{Daos[item][0:4]}'}
             } for item in Daos.keys()
        ]
        nodes += [{"name": item[0],
                   "symbolSize": min(60, 10 * len(item[1])),
                   'belongs': item[1],
                   'value': '   '.join([f'【{each}】{Daos[each][0:min(20, len(Daos[each]))]}' for each in item[1]])} for
                  item in self.relations
                  ]
        return nodes

    def get_links(self):
        links = []
        for node in self.nodes:
            if 'belongs' in node:  # 关键字节点
                for each in node['belongs']:
                    links.append({"source": node.get("name"), "target": str(each)})
        return links

    def get_graph(self, nodes, links):
        graph = Graph(init_opts=opts.InitOpts(width="1500px",
                                              height="1000px",
                                              animation_opts=opts.AnimationOpts(animation=False)),
                      )
        graph.add("", nodes, links, repulsion=8000, tooltip_opts=opts.TooltipOpts(
            formatter="<div style='width:600px; white-space:pre-wrap'>{c}</div>"),
                  is_draggable=False)
        graph.set_global_opts(title_opts=opts.TitleOpts(title="Graph-基本示例"))
        graph.render()
        return graph

    def run(self, keywords=None):
        self.relations = self.init_relations(keywords)
        self.nodes = self.get_node_list()
        self.links = self.get_links()
        self.get_graph(nodes=self.nodes, links=self.links)


if __name__ == '__main__':
    graph = DaoGraph()
    graph.run()
