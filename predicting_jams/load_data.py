#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psycopg2
from predicting_jams.parse import parse_street_graph, parse_jams_data


def main():
    conn_string = "host='localhost' port='25432' dbname='predicting-jams' user='docker' password='docker'"
    print "Connecting to database\n	->%s" % (conn_string)
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    print "Connected!"
    (nodes, edges) = parse_street_graph()
    print "Inserting nodes."
    for node in nodes:
        cursor.execute("INSERT INTO node (id, geometry) VALUES (%s, ST_MakePoint(%s, %s))" % (node.id, node.long, node.lat))
    conn.commit()
    print "Inserting nodes finished."

    print "Inserting edges."
    for edge in edges:
        cursor.execute("INSERT INTO edge (node1_id, node2_id, distance, lanes, max_velocity) VALUES (%s, %s, %s, %s, %s)" % (edge.id1, edge.id2, edge.distance, edge.lanes, edge.max_velocity))
    conn.commit()
    print "Inserting edges finished."

    jams = parse_jams_data()
    jam_id = 1
    print "Inserting jams."
    for jam in jams:
        print "Inserting jam %d." % (jam_id)
        cursor.execute("INSERT INTO jam (id) VALUES (%s)" % (jam_id))
        for removed in jam.removed:
            cursor.execute("INSERT INTO jam_removed (jam_id, node1_id, node2_id) VALUES (%s, %s, %s)" % (jam_id, removed.id1, removed.id2))
        for in_20 in jam.in_20:
            cursor.execute("INSERT INTO jam_20m (jam_id, node1_id, node2_id) VALUES (%s, %s, %s)" % (jam_id, in_20.id1, in_20.id2))
        for in_40 in jam.in_40:
            cursor.execute("INSERT INTO jam_40m (jam_id, node1_id, node2_id) VALUES (%s, %s, %s)" % (jam_id, in_40.id1, in_40.id2))
        jam_id += 1
    conn.commit()
    print "Inserting jams finished."

if __name__ == "__main__":
    main()
