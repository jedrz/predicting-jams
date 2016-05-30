#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psycopg2


def connect():
    conn_string = "host='localhost' port='25432' dbname='predicting-jams' user='docker' password='docker'"
    conn = psycopg2.connect(conn_string)
    return conn


def _query(query_str, fetch_result_fn):
    with connect() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query_str)
            return fetch_result_fn(cursor)


def query_one(query_str):
    return _query(query_str, lambda cursor: cursor.fetchone())


def query_all(query_str):
    return _query(query_str, lambda cursor: cursor.fetchall())
