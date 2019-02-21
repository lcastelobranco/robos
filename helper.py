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



def error(msg):
    print msg
    sys.exit(0)



import socket
import socks


def connectTor():
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,"127.0.0.1",9050,True, 'socks5_user','socks_pass')
    socket.socket = socks.socksocket
    print "\n Connected to Tor"

def newidentity():
    socks.setdefaultproxy()
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect(("127.0.0.1",9051))
    s.send("AUTHENTICATE\r\n")
    response = s.recv(128)
    if response.startswith("250"):
        s.send("SIGNAL NEWNYM\r\n")
        s.close()
        connectTor()

from twilio.rest import Client

def send_sms(msg):
    account_sid = 'AC897ef311333782e8cbb17986239d508a'
    auth_token = 'f87ec6eee0be40c9502b4946c1f4cfb0'
    client = Client(account_sid, auth_token)
    message = client.messages.create(body=msg,from_='+12513336519', to='+5511955008164')
    #print(message.sid)