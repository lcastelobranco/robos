#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import datetime
from helper import *



def parser(data, linha):
    str_sql = "INSERT INTO composicaoibov (data,ticker,nome,tipo,quantidadeteorica,participacao) values (%s,%s,%s,%s,%s,%s)"
    cursor.execute(str_sql, tuple([data] + linha.split('\n\n')[1:-1]))
    conn.commit()




conn ,cursor,engine = conection("dados")
lista = contexto(cursor,"composicaoibov")



url = "http://bvmf.bmfbovespa.com.br/indices/ResumoCarteiraTeorica.aspx?Indice=IBOV&idioma=pt-br"



html = requests.post(url)
soup = BeautifulSoup(html.text,'html.parser')
data = '20'+'-'.join(soup.find_all(id="ctl00_contentPlaceHolderConteudo_lblTitulo")[0].text.split()[-1].split('/')[::-1])


try:
    linhas = map(lambda x: x.text.replace('.','').replace(',','.'), soup.table.find_all('tr'))
    if data not in lista:
        for linha in linhas[2:]:
            parser(data,linha)
    if data == datetime.datetime.now().strftime("%Y-%m-%d"):
        with open(r"C:\Users\luiz\PycharmProjects\robos\checklist.txt", 'r') as checklist:
            texto = checklist.read().replace('composicaoibov\n', '')
        with open(r"C:\Users\luiz\PycharmProjects\robos\checklist.txt", 'w') as checklist:
                checklist.write(texto)


except:
    error('algum erro do processo em geral')