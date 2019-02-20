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
    cursor.execute("Select data from ptax order by data desc")
    return map( lambda x : x[0].strftime("%Y-%m-%d")  ,cursor.fetchall())

def error():
    print 'deu erro, nao sei qual eh.'
    sys.exit(0)


def parser(data, compra, venda):
    str_sql = "INSERT INTO ptax (data,compra,venda) values (%s,%s,%s)"
    cursor.execute(str_sql, (data,  compra,venda))
    conn.commit()




conn ,cursor= conection()
lista = contexto(cursor)


url = "https://ptax.bcb.gov.br/ptax_internet/consultaBoletim.do?method=consultarBoletim"

hoje = datetime.datetime.now()
params = {
"RadOpcao" : "1",
"DATAINI" : (hoje + datetime.timedelta(-6)).strftime("%d/%m/%Y") ,
"DATAFIM" : hoje.strftime("%d/%m/%Y") ,
"ChkMoeda" : "61"
}

html = requests.post(url,data= params)
soup = BeautifulSoup(html.text,'html.parser')

try:
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