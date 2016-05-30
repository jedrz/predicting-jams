#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import namedtuple

from predicting_jams import db
from predicting_jams.parse import Jam


OrderedEdge = namedtuple('OrderedEdge', ['id1', 'id2', 'event_id'])


def _precision(predicted, target, i):
    predicted = set(predicted[:i])
    target = set(target[:i])
    in_common = predicted & target
    return len(in_common) / i


def quality(predicted, target):
    n = max(len(predicted), len(target))
    precisions = [_precision(predicted, target, i) for i in range(1, n + 1)]
    return sum(precisions) / n


def get_random_example():
    jam_id = db.query_one("SELECT id FROM jam_test ORDER BY random() LIMIT 1")[0]

    def query_segments(table_name):
        segments = db.query_all("""
        SELECT node1_id, node2_id, event_id
        FROM {}
        WHERE jam_id = {}
        ORDER BY event_id
        """.format(table_name, jam_id))
        return [OrderedEdge._make(segment) for segment in segments]

    removed = query_segments('jam_removed')
    in_20 = query_segments('jam_20m')
    in_40 = query_segments('jam_40m')
    return Jam(removed, in_20, in_40)


def _query_geometry(node_id):
    return db.query_one("SELECT ST_AsText(geometry) FROM node WHERE id = {}"
                        .format(node_id))[0]

# Looks like there is a lot of identical segments...
def query_closest_segments(edge):
    node1_geom = _query_geometry(edge.id1)
    node2_geom = _query_geometry(edge.id2)
    return db.query_all("""
    SELECT
      jam_20m_train.*,
      (ST_Distance('SRID=4326;{node1_geom}'::geography, node1.geometry)
        + ST_Distance('SRID=4326;{node2_geom}'::geography, node2.geometry)
        + 0.1)
        * power(abs(event_id - {event_id}), 2) as weight
    FROM jam_20m_train
    JOIN node node1 ON node1_id = node1.id
    JOIN node node2 ON node2_id = node2.id
    ORDER BY weight
    LIMIT 10000
    """.format(node1_geom=node1_geom,
               node2_geom=node2_geom,
               event_id=edge.event_id))
