#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import psycopg2
import sys
from bs4 import BeautifulSoup
import datetime


import socket
import socks
def connectTor():
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,"127.0.0.1",9050,True, 'socks5_user','socks_pass')
    socket.socket = socks.socksocket
    print "\n Connected to Tor"
    print BeautifulSoup(requests.get('https://check.torproject.org/?lang=pt_BR').text, 'html.parser').html.body.find_all('div')[1].find_all('p')[0].strong.text

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

connectTor()


def conection():
    #engine = create_engine('postgresql+psycopg2://postgres:L30051992z@localhost:5432/dados')
    conn = psycopg2.connect(host="localhost", database="dados", user="postgres", password="L30051992z")
    return conn,conn.cursor()

def contexto(cursor):
    cursor.execute("Select distinct data from auxptax")
    return cursor

def error(aviso=''):
    if aviso:
        print aviso
    else:
        print 'deu erro, nao sei qual eh.'
        sys.exit(0)





conn ,cursor= conection()

menor = min(map( lambda x : x[0],contexto(cursor).fetchall()))
for i in range(1,1500):
    #url = "https://ptax.bcb.gov.br/ptax_internet/consultaBoletim.do?method=gerarCSVTodasAsMoedas&id="+str(i)
    url = "https://ptax.bcb.gov.br/ptax_internet/consultaBoletim.do?method=consultarBoletim"
    params = {
    "RadOpcao" : "2",
    "DATAINI"  : ( menor - datetime.timedelta(i)).strftime("%d/%m/%Y"),
    "DATAFIM"  : "",
    "ChkMoeda" : "1"}

    try:
        html = requests.post(url, data=params, allow_redirects=True)
    except:
        newidentity()
        html = requests.post(url, data=params, allow_redirects=True)

    soup = BeautifulSoup(html.text, 'html.parser')
    try:
        linhas = map(lambda x: x.text.replace(',', '.').split(), soup.find_all('tr')[1:])
        linhas = filter(lambda x : len(x) == 7 and len(x[0]) == 3,linhas)
        data = '-'.join(soup.html.body.div.text.split('\n')[1].strip('.').split(' ')[-1].split('/')[::-1])
        if len(data) > 1:
            if data != (menor - datetime.timedelta(i)).strftime("%Y-%m-%d"):
                print data,(menor - datetime.timedelta(i)).strftime("%Y-%m-%d")
                error('datas nao batem')


            if data not in map( lambda x : x[0].strftime("%Y-%m-%d")  ,contexto(cursor).fetchall()):
                for linha in linhas:
                    str_sql = "INSERT INTO auxptax (data,codigo,tipo,moeda,realcompra,realvenda,usdcompra,usdvenda) values (%s,%s,%s,%s,%s,%s,%s,%s)"



                    cursor.execute(str_sql,tuple( [data] + linha))
                    conn.commit()
            else:
                error('esta repetindo data')
    except:
        error()