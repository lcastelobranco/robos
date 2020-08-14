import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
from helper import *

conn ,cursor,engine= conection("robos_b3")
lista = contexto(cursor,"btc")


def processar(RS,qtd):
    aux = RS.split('.')
    if len(aux)==1:
        dinheiro = int(aux[0]+'00')
    else:
        if len(aux[1]) == 1:
            dinheiro = int(aux[0]+aux[1]+'0')
        else:
            dinheiro = int(aux[0]+aux[1])
    quantidade = int(qtd)*100
    aux = str(dinheiro/quantidade).split('.')
    aux = aux[0]+'.'+aux[1][:7]
    return str(aux)


try:
    a = requests.get('http://www.b3.com.br/pt_br/produtos-e-servicos/emprestimo-de-ativos/renda-variavel/posicoes-em-aberto/')
    data = re.findall(r'Dados de Fechamento do Pregão de (.*?)<',a.text)[0]

    if '-'.join(data.split('/')[::-1]) not in lista:
        h = "http://www.b3.com.br/pt_br/produtos-e-servicos/emprestimo-de-ativos/renda-variavel/posicoes-em-aberto/renda-variavel-8AE490C9701B5B35017039842ACE1F91.htm?data="+data+"&f=0"
        r = requests.post(h,params={"data": data})
        soup = BeautifulSoup(r.content, 'html.parser')
        #isin = pd.read_sql("select ticker,isin from btc",conn)
        for t in range(len(soup.tbody.find_all("td")[0::5])):
            str_sql = "INSERT INTO btc (data,ticker,nome,tipo_papel,isin,qtd_total,avg_price,fator_cot,volume) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            
            lista =  ["'"+'-'.join(data.split('/')[::-1])+"'"]
            lista.append(list(map(lambda x: x.text.strip().upper(),soup.tbody.find_all("td")[0::5]))[t])
            lista.append(list(map(lambda x: x.text.strip().upper().replace("B3 S.A. ¿ BRASI","B3 S.A. - BRASI"),soup.tbody.find_all("td")[1::5]))[t])
            lista.append(list(map(lambda x: x.text.strip().upper(),soup.tbody.find_all("td")[2::5]))[t])
            #lista.append(isin[isin.ticker==lista[1]].values[0][1])
            lista.append('')
            lista.append(list(map(lambda x: x.text.strip().replace(".",'').replace(",","."),soup.tbody.find_all("td")[3::5]))[t])
            lista.append('')
            lista.append('1')
            lista.append(list(map(lambda x: x.text.strip().replace(".",'').replace(",","."),soup.tbody.find_all("td")[4::5]))[t])
            
            lista[6] = processar(lista[8],lista[5])
            
            cursor.execute(str_sql, tuple(lista))
        conn.commit()
        with open(r"checklist.txt", 'a') as checklist:
            checklist.writelines('btc\n')


except:
    #print(t,lista)
    print('BTC - algum erro do processo em geral')