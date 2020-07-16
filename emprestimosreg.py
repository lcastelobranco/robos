#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
from helper import *

conn ,cursor,engine= conection("robos_b3")
lista = contexto(cursor,"emprestimosreg")

try:
    a = requests.get('http://www.b3.com.br/pt_br/produtos-e-servicos/emprestimo-de-ativos/renda-variavel/s_empreg_ativos/')
    data = re.findall(r'Dados de Fechamento do Pregão de (.*?)<',a.text)[0]
    

    if data not in lista:
        h = "http://www.b3.com.br/pt_br/produtos-e-servicos/emprestimo-de-ativos/renda-variavel/s_empreg_ativos/renda-variavel-8AA8D0CD701B61040170400B64840F04.htm?data="+data+"&f=0"
        r = requests.post(h,params={"data": data})
        soup = BeautifulSoup(r.content, 'html.parser')
        for t in range(len(soup.tbody.find_all("td")[0::11])):
            str_sql = "INSERT INTO emprestimosreg  (data,ticker,nome,n_contratos,qtd_shs,volume,doador_min,doador_med,doador_max,tomador_min,tomador_med,tomador_max) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            
            lista =  11*[""]
            lista[0] =list(map(lambda x: x.text.upper(),soup.tbody.find_all("td")[0::11]))[t]
            lista[1] =list(map(lambda x: x.text.upper().replace("B3 S.A. ¿ BRASI","B3 S.A. - BRASI"),soup.tbody.find_all("td")[1::11]))[t]
            for i in range(2,11,1):
                lista[i] = list(map(lambda x: x.text.replace("%","").replace(".",'').replace(",","."),soup.tbody.find_all("td")[i::11]))[t]
            cursor.execute(str_sql, tuple(["'"+'-'.join(data.split('/')[::-1])+"'"]+lista))
        conn.commit()
        with open(r"checklist.txt", 'a') as checklist:
            checklist.writelines('emprestimosreg\n')


except:
    #print(t,lista)
    print('EmprestimosReg algum erro do processo em geral')