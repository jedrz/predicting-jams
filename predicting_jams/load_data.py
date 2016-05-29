#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

from predicting_jams import db
from predicting_jams.parse import parse_street_graph, parse_jams_data


TRAIN_DATA_RATIO = 0.95


def main():
    print("Connecting to database.")
    conn = db.connect()
    cursor = conn.cursor()
    print("Connected!")
    (nodes, edges) = parse_street_graph()
    print("Inserting nodes.")
    for node in nodes:
        cursor.execute("INSERT INTO node (id, geometry) VALUES ({}, ST_MakePoint({}, {}))".format(node.id, node.long, node.lat))
    conn.commit()
    print("Inserting nodes finished.")

    print("Inserting edges.")
    for edge in edges:
        cursor.execute("INSERT INTO edge (node1_id, node2_id, distance, lanes, max_velocity) VALUES ({}, {}, {}, {}, {})".format(edge.id1, edge.id2, edge.distance, edge.lanes, edge.max_velocity))
    conn.commit()
    print("Inserting edges finished.")

    jams = parse_jams_data()
    jam_id = 1
    print("Inserting jams.")
    for jam in jams:
        print("Inserting jam {}.".format(jam_id))
        cursor.execute("INSERT INTO jam (id) VALUES ({})".format(jam_id))
        for removed in jam.removed:
            cursor.execute("INSERT INTO jam_removed (jam_id, node1_id, node2_id) VALUES ({}, {}, {})".format(jam_id, removed.id1, removed.id2))
        for in_20 in jam.in_20:
            cursor.execute("INSERT INTO jam_20m (jam_id, node1_id, node2_id) VALUES ({}, {}, {})".format(jam_id, in_20.id1, in_20.id2))
        for in_40 in jam.in_40:
            cursor.execute("INSERT INTO jam_40m (jam_id, node1_id, node2_id) VALUES ({}, {}, {})".format(jam_id, in_40.id1, in_40.id2))
        jam_id += 1
    conn.commit()
    print("Inserting jams finished.")

    print("Splitting jams into train and test data.")
    cursor.execute("SELECT id FROM jam")
    jams_result = cursor.fetchall()
    jam_ids = list(map(lambda row: row[0], jams_result))
    random.shuffle(jam_ids)
    train_data_len = int(TRAIN_DATA_RATIO * len(jam_ids))
    train_jam_ids = sorted(jam_ids[:train_data_len])
    test_jam_ids = sorted(jam_ids[train_data_len:])
    for train_jam_id in train_jam_ids:
        cursor.execute("INSERT INTO jam_train (id) VALUES ({})".format(train_jam_id))
    for test_jam_id in test_jam_ids:
        cursor.execute("INSERT INTO jam_test (id) VALUES ({})".format(test_jam_id))
    conn.commit()
    print("Splitting jams finished.")


if __name__ == "__main__":
    main()
