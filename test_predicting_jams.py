#!/usr/bin/env python
# -*- coding: utf-8 -*-

from predicting_jams import *

def test_sample_function():
    assert sample_function() == 42

def test_parse_street_graph_lines():
    input = '''
Nodes:    
Node_id Latitude Longitude  
26063726 52.1528 21.0174  
26063729 52.1424 21.0176  
Edges:    
Node1_id Node2_id Distance(km) Nr_of_lanes Avg_max_velocity
26405552 26063726 0.022 2 70
254508217 261239412 0.004 1 60
'''

    (nodes, edges) = parse_street_graph_lines(input.splitlines())

    assert len(nodes) == 2
    assert nodes[0] == (26063726, 52.1528, 21.0174)
    assert len(edges) == 2
    assert edges[0] == (26405552, 26063726, 0.022, 2, 70)
