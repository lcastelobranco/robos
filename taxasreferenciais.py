#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import psycopg2
from bs4 import BeautifulSoup
import datetime
import sys


def conection():
    #engine = create_engine('postgresql+psycopg2://postgres:L30051992z@localhost:5432/dados')
    conn = psycopg2.connect(host="localhost", database="dados", user="postgres", password="L30051992z")
    return conn,conn.cursor()

def contexto(cursor):
    cursor.execute("Select data from taxasreferenciais order by data desc")
    return map( lambda x : x[0].strftime("%Y-%m-%d")  ,cursor.fetchall())

def error():
    print 'deu erro, nao sei qual eh.'
    sys.exit(0)


def parser(data, compra, venda):
    str_sql = "INSERT INTO taxasreferenciais (data,ref3600,ref1080) values (%s,%s,%s)"
    cursor.execute(str_sql, (data, ref3600, ref1080))
    conn.commit()




conn ,cursor= conection()
lista = contexto(cursor)


hoje = datetime.datetime.now()
hoje = datetime.datetime.now() + datetime.timedelta(-6)

url = "http://www2.bmf.com.br/pages/portal/bmfbovespa/lumis/lum-taxas-referenciais-bmf-ptBR.asp?Data=" + hoje.strftime("%d/%m/%Y")+ "&slcTaxa=PRE"
html = requests.get(url)
soup = BeautifulSoup(html.text,'html.parser')
#pdb.set_trace()
print 'sdfsd'
0/0
try:
    0/0
    datas = map( lambda x : '-'.join(x.text.split('/')[::-1]) ,soup.table.find_all('td')[0:-1:4])
    compras = map( lambda x : x.text.replace(',','.') ,soup.table.find_all('td')[2:-1:4])
    vendas = map( lambda x : x.text.replace(',','.') ,soup.table.find_all('td')[3:-1:4])

    if len(datas) == len(compras) == len(vendas):
        for i in range(len(datas)):
            if datas[i] not in lista:
                parser(datas[i],compras[i],vendas[i])
                if datas[i] == hoje.strftime("%Y-%m-%d"):
                    with open(r"C:\Users\luiz\PycharmProjects\robos\checklist.txt", 'r') as checklist:
                        texto = checklist.read().replace('ptax\n', '')
                    with open(r"C:\Users\luiz\PycharmProjects\robos\checklist.txt", 'w') as checklist:
                        checklist.write(texto)
    else:
        error()

except:
    error()