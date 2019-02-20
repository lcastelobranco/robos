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
    cursor.execute("Select data from composicaoibov order by data desc")
    return map( lambda x : x[0].strftime("%Y-%m-%d")  ,cursor.fetchall())

def error():
    print 'deu erro, nao sei qual eh.'
    sys.exit(0)


def parser(data, linha):
    str_sql = "INSERT INTO composicaoibov (data,ticker,nome,tipo,quantidadeteorica,participacao) values (%s,%s,%s,%s,%s,%s)"
    cursor.execute(str_sql, tuple([data] + linha.split('\n\n')[1:-1]))
    conn.commit()




conn ,cursor= conection()
lista = contexto(cursor)


url = "http://bvmf.bmfbovespa.com.br/indices/ResumoCarteiraTeorica.aspx?Indice=IBOV&idioma=pt-br"



html = requests.post(url)
soup = BeautifulSoup(html.text,'html.parser')
data = '20'+'-'.join(soup.find_all(id="ctl00_contentPlaceHolderConteudo_lblTitulo")[0].text.split()[-1].split('/')[::-1])


try:
    #if map(lambda x: x.text, soup.table.find_all('tr'))[0].strip() == u'Código AçãoTipoQtde. TeóricaPart. (%)' :
    #    if map(lambda x: x.text, soup.table.find_all('tr'))[1].split()[0:4] == [u'Quantidade', u'Teórica', u'Total', u'Redutor'] :
    linhas = map(lambda x: x.text.replace('.','').replace(',','.'), soup.table.find_all('tr'))
    if data not in lista:
        for linha in linhas[2:]:
            parser(data,linha)
    if data == datetime.datetime.now().strftime("%Y-%m-%d"):
        with open(r"C:\Users\luiz\PycharmProjects\robos\checklist.txt", 'r') as checklist:
            texto = checklist.read().replace('composicaoibov\n', '')
        with open(r"C:\Users\luiz\PycharmProjects\robos\checklist.txt", 'w') as checklist:
                checklist.write(texto)
    #    else:
    #        error()
    #else:
    #    error()

except:
    error()