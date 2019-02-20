#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psycopg2
from sqlalchemy import create_engine


def conection(database):
    engine = create_engine('postgresql+psycopg2://postgres:L30051992z@localhost:5432/'+database)
    conn = psycopg2.connect(host="localhost", database=database, user="postgres", password="L30051992z")
    return conn,conn.cursor(),engine

def contexto(cursor,tabela):
    cursor.execute("Select data from "+tabela+" order by data desc")
    return map( lambda x : x[0].strftime("%Y-%m-%d"), cursor.fetchall())
