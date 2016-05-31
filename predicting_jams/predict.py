#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import namedtuple
import math

from predicting_jams import db
from predicting_jams import parse
from predicting_jams.parse import Jam, SimpleEdge


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
        SELECT node1_id, node2_id
        FROM {}
        WHERE jam_id = {}
        ORDER BY event_id
        """.format(table_name, jam_id))
        return [SimpleEdge._make(segment) for segment in segments]

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


def weight_segments(test_segments, train_segments):
    p = 10
    return 1 / math.log((abs(len(test_segments) - len(train_segments)) + p), p)


def similarity_segments(test_segments, train_segments):
    similarity = 0
    segments_len = len(test_segments)
    for train_index, train_segment in enumerate(train_segments):
        if train_segment in test_segments:
            test_index = test_segments.index(train_segment)
            similarity += segments_len - abs(test_index - train_index)
    return weight_segments(test_segments, train_segments) * similarity


def sort_jams_by_similarity(segments, jams):
    #return list(reversed(sorted([similarity_segments(segments, jam.in_20) for jam in jams])))
    return sorted(jams, key=lambda jam: similarity_segments(segments, jam.in_20), reverse=True)


def extract_in_40_segments(jams):
    return set([segment
                for jam in jams
                for segment in jam.in_40])


def predict_length(jams):
    lengths = [len(jam.in_40) for jam in jams]
    return round(sum(lengths) / len(lengths))


def compute_mean_position(segment, jams):
    positions = [jam.in_40.index(segment) for jam in jams if segment in jam.in_40]
    return sum(positions) / len(positions)


def compute_frequency(segment, jams):
    return len(list(filter(lambda jam: segment in jam.in_40, jams)))


def build_mean_positions_dict(segments, jams):
    return {segment: compute_mean_position(segment, jams)
            for segment in segments}


def build_frequencies_dict(segments, jams):
    return {segment: compute_frequency(segment, jams)
            for segment in segments}


def get_segments_around_position(position, mean_positions):
    return [segment
            for segment, mean_position in mean_positions.items()
            if round(mean_position) == position + 1]


def get_possible_segments_at_position(position, mean_positions):
    segments = get_segments_around_position(position, mean_positions)
    position_diff = 1
    while not segments:
        segments += get_segments_around_position(position + position_diff, mean_positions)
        segments += get_segments_around_position(position - position_diff, mean_positions)
        position_diff += 1
    return segments


def predict_segment(segments, frequencies):
    return list(sorted(segments, key=lambda segment: frequencies[segment]))[-1]


def predict_from_jams(jams):
    all_in_40_segments = extract_in_40_segments(jams)
    length = predict_length(jams[:(len(jams) // 10)])
    all_mean_positions = build_mean_positions_dict(all_in_40_segments, jams)
    all_frequencies = build_frequencies_dict(all_in_40_segments, jams)
    in_40 = []
    for position in range(length):
        possible_segments = get_possible_segments_at_position(position, all_mean_positions)
        segment = predict_segment(possible_segments, all_frequencies)
        del all_mean_positions[segment]
        in_40.append(segment)
    return in_40


def predict(jam):
    jams = parse.parse_jams_09_data()
    ranked_jams = sort_jams_by_similarity(jam.in_20, jams)
    return predict_from_jams(ranked_jams[:200])


def predict_and_evaluate(jam):
    predicted_in_40 = predict(jam)
    return quality(predicted_in_40, jam.in_40)
