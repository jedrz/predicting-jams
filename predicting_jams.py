#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import namedtuple

STREET_GRAPH_PATH = 'data/street_graph.txt'

def sample_function():
    return 42

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
