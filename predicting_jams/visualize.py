#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt

from predicting_jams.parse import parse_street_graph, parse_jams_data


def build_node_dict(nodes):
    return {n.id: n for n in nodes}


def display_map(node_dict, edges):
    x = []
    y = []
    for e in edges:
        n1 = node_dict[e.id1]
        n2 = node_dict[e.id2]
        x.extend([n1.long, n2.long])
        y.extend([n1.lat, n2.lat])
    plt.plot(x, y, '.-', c='g')


def display_jam(jam, node_dict):
    display_labels(jam.removed, 'r', node_dict)
    display_labels(jam.in_20, 'f', node_dict)
    display_labels(jam.in_40, 's', node_dict)


def display_labels(edges, prefix, node_dict):
    for i, e in enumerate(edges):
        display_and_annote_node(node_dict[e.id1], prefix, i, True)
        display_and_annote_node(node_dict[e.id2], prefix, i, False)


def display_and_annote_node(node, prefix, index, should_annotate):
    plt.scatter([node.long], [node.lat], s=100, c='r', marker='x')
    if should_annotate:
        plt.annotate('{}{}'.format(prefix, index), (node.long, node.lat))


def display(should_display_map=False, should_display_jam=True, jam_index=0):
    (nodes, edges) = parse_street_graph()
    jam = parse_jams_data()[jam_index]
    node_dict = build_node_dict(nodes)
    if should_display_map:
        display_map(node_dict, edges)
    if should_display_jam:
        display_jam(jam, node_dict)
    plt.show()


if __name__ == '__main__':
    display()
