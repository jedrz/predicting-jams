#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import namedtuple


STREET_GRAPH_PATH = 'data/street_graph.txt'
JAMS_TRAINING_PATH = 'data/jams_training.txt'


Point = namedtuple('Point', ['id', 'lat', 'long'])
Edge = namedtuple('Edge', ['id1', 'id2', 'distance', 'lanes', 'max_velocity'])
Jam = namedtuple('Jam', ['removed', 'in_20', 'in_40'])
SimpleEdge = namedtuple('SimpleEdge', ['id1', 'id2'])


def parse_street_graph():
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
    return Point(id=elements[0],
                 lat=float(elements[1]),
                 long=float(elements[2]))


def parse_edge(elements):
    return Edge(id1=elements[0],
                id2=elements[1],
                distance=float(elements[2]),
                lanes=int(elements[3]),
                max_velocity=int(elements[4]))


def parse_jams_data():
    with open(JAMS_TRAINING_PATH) as f:
        return parse_jams_data_lines(f.readlines())


def parse_jams_data_lines(lines):
    return [parse_jam_line(line.strip()) for line in lines]


def parse_jam_line(line):
    removed = line.split(' ')[:5]
    removed = list(map(parse_simple_edge, removed))
    (in_20, in_40) = line.split(':')
    in_20 = list(map(parse_simple_edge, in_20.split(' ')[5:]))
    in_40 = list(map(parse_simple_edge, in_40.split(' ')))
    return Jam(removed, in_20, in_40)


def parse_simple_edge(simple_edge):
    simple_edge = simple_edge.split('_')
    return SimpleEdge._make(simple_edge)
