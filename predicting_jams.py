#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import namedtuple

import matplotlib.pyplot as plt


STREET_GRAPH_PATH = 'data/street_graph.txt'


Point = namedtuple('Point', ['id', 'lat', 'long'])
Edge = namedtuple('Edge', ['id1', 'id2', 'distance', 'lanes', 'max_velocity'])


def parse_stree_graph():
    with open(STREET_GRAPH_PATH) as f:
        return parse_street_graph_lines(f.readlines())


def parse_street_graph_lines(lines):
    nodes = []
    edges = []
    for line in lines:
        if not line or not line[0].isdigit():
            continue
        elements = line.strip().split(' ')
        if len(elements) == 3:
            nodes.append(parse_node(elements))
        else:
            edges.append(parse_edge(elements))
    return (nodes, edges)


def parse_node(elements):
    return Point(id=int(elements[0]),
                 lat=float(elements[1]),
                 long=float(elements[2]))


def parse_edge(elements):
    return Edge(id1=int(elements[0]),
                id2=int(elements[1]),
                distance=float(elements[2]),
                lanes=int(elements[3]),
                max_velocity=int(elements[4]))


def display_map():
    (nodes, edges) = parse_stree_graph()
    node_dict = {n.id: n for n in nodes}
    x = []
    y = []
    for e in edges:
        n1 = node_dict[e.id1]
        n2 = node_dict[e.id2]
        x.extend([n1.long, n2.long])
        y.extend([n1.lat, n2.lat])
    plt.plot(x, y, '.-')
