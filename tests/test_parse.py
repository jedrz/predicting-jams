#!/usr/bin/env python
# -*- coding: utf-8 -*-

from context import predicting_jams
from predicting_jams import parse
from predicting_jams.parse import *


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
    assert nodes[0] == ('26063726', 52.1528, 21.0174)
    assert len(edges) == 2
    assert edges[0] == ('26405552', '26063726', 0.022, 2, 70)


def test_parse_jams_data():
    input = '32049370_32049364 32597785_32599710 251856122_224814449 260152955_260152954 255309049_254340652 35967065_27166981 254021308_29169080:254021581_32320961 31897831_33242043'

    jams = parse_jams_data_lines([input])

    assert len(jams) == 1
    jam = jams[0]
    assert len(jam.removed) == 5
    assert jam.removed[0] == ('32049370', '32049364')
    assert len(jam.in_20) == 2
    assert jam.in_20[0] == ('35967065', '27166981')
    assert len(jam.in_40) == 2
    assert jam.in_40[0] == ('254021581', '32320961')
