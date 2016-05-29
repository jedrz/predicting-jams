#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psycopg2


def connect():
    conn_string = "host='localhost' port='25432' dbname='predicting-jams' user='docker' password='docker'"
    conn = psycopg2.connect(conn_string)
    return conn
