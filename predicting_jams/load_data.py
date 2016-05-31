#!/usr/bin/env python
# -*- coding: utf-8 -*-

from predicting_jams import db
from predicting_jams.parse import parse_street_graph, parse_jams_09_data, parse_jams_01_data


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

    train_jams = parse_jams_09_data()
    test_jams = parse_jams_01_data()
    jams = train_jams + test_jams
    jam_id = 1
    print("Inserting jams.")
    for jam in jams:
        print("Inserting jam {}.".format(jam_id))
        cursor.execute("INSERT INTO jam (id) VALUES ({})".format(jam_id))
        for i, removed in enumerate(jam.removed):
            cursor.execute("INSERT INTO jam_removed (jam_id, event_id, node1_id, node2_id) VALUES ({}, {}, {}, {})".format(jam_id, i, removed.id1, removed.id2))
        for i, in_20 in enumerate(jam.in_20):
            cursor.execute("INSERT INTO jam_20m (jam_id, event_id, node1_id, node2_id) VALUES ({}, {}, {}, {})".format(jam_id, i, in_20.id1, in_20.id2))
        for i, in_40 in enumerate(jam.in_40):
            cursor.execute("INSERT INTO jam_40m (jam_id, event_id, node1_id, node2_id) VALUES ({}, {}, {}, {})".format(jam_id, i, in_40.id1, in_40.id2))
        jam_id += 1
    conn.commit()
    print("Inserting jams finished.")

    print("Splitting jams into train and test data.")
    train_jam_ids = range(1, len(train_jams) + 1)
    test_jam_ids = range(len(train_jams) + 1, len(jams) + 1)
    for train_jam_id in train_jam_ids:
        cursor.execute("INSERT INTO jam_train (id) VALUES ({})".format(train_jam_id))
    for test_jam_id in test_jam_ids:
        cursor.execute("INSERT INTO jam_test (id) VALUES ({})".format(test_jam_id))
    conn.commit()
    print("Splitting jams finished.")

    print("Refreshing train views.")
    cursor.execute("REFRESH MATERIALIZED VIEW jam_removed_train")
    cursor.execute("REFRESH MATERIALIZED VIEW jam_20m_train")
    cursor.execute("REFRESH MATERIALIZED VIEW jam_40m_train")
    conn.commit()
    print("Refreshing train views finished.")


if __name__ == "__main__":
    main()
