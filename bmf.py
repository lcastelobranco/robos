from helper import *
import requests
from bs4 import BeautifulSoup
import re
import datetime

def parser(data_arquivo,dados):
    aux = ['Pessoa Jurídica Financeira', 'Bancos', "DTVM'S e Corretoras de Valores",'Investidor Institucional', "Invest Institucional Nacional",'Investidores Não Residentes', 'Inv Não Residente - Res2689','Pessoa Jurídica Não Financeira', 'Pessoa Física', 'Total Geral']
    if dados[::5] == aux:
        for i in range(0, len(dados)-5, 5):
            str_sql = "INSERT INTO bmf (data,tipo,compravenda,n_contratos) values (%s,%s,%s,%s)"
            cursor.execute(str_sql, (data_arquivo, dados[0+i], 'C', dados[1+i]))
            cursor.execute(str_sql, (data_arquivo, dados[0+i], 'V', dados[3+i]))
        conn.commit()
    elif dados[::5] == ['Pessoa Jurídica Financeira', 'Bancos', "DTVM'S e Corretoras de Valores", "Outras Jurídicas Financeiras",'Investidor Institucional', "Invest Institucional Nacional", 'Investidores Não Residentes','Inv Não Residente - Res2689', 'Pessoa Jurídica Não Financeira', 'Pessoa Física']:
        for i in range(0, len(dados), 5):
            str_sql = "INSERT INTO bmf (data,tipo,compravenda,n_contratos) values (%s,%s,%s,%s)"
            cursor.execute(str_sql, (data_arquivo, dados[0 + i], 'C', dados[1 + i]))
            cursor.execute(str_sql, (data_arquivo, dados[0 + i], 'V', dados[3 + i]))

        conn.commit()
    elif dados[::5]  == ['Pessoa Jurídica Financeira', 'Bancos', "DTVM'S e Corretoras de Valores", "Outras Jurídicas Financeiras",'Investidor Institucional', "Invest Institucional Nacional", 'Invest Institucional Estrangeiro', 'Pessoa Jurídica Não Financeira', 'Pessoa Física','Total Geral']:
        for i in range(0, len(dados)-5, 5):
            str_sql = "INSERT INTO bmf (data,tipo,compravenda,n_contratos) values (%s,%s,%s,%s)"
            cursor.execute(str_sql, (data_arquivo, dados[0 + i], 'C', dados[1 + i]))
            cursor.execute(str_sql, (data_arquivo, dados[0 + i], 'V', dados[3 + i]))
        conn.commit()
    elif dados[::5]  == ['Pessoa Jurídica Financeira', 'Bancos', "DTVM'S e Corretoras de Valores","Outras Jurídicas Financeiras", 'Investidor Institucional', "Invest Institucional Nacional",'Invest Institucional Estrangeiro', 'Fundo de Conversao de Capital Estrangeiro', 'Pessoa Jurídica Não Financeira','Pessoa Física']:
        for i in range(0, len(dados), 5):
            str_sql = "INSERT INTO bmf (data,tipo,compravenda,n_contratos) values (%s,%s,%s,%s)"
            cursor.execute(str_sql, (data_arquivo, dados[0 + i], 'C', dados[1 + i]))
            cursor.execute(str_sql, (data_arquivo, dados[0 + i], 'V', dados[3 + i]))
        conn.commit()
    elif dados[::5][:-1] == ['Pessoa Jurídica Financeira', 'Bancos', "DTVM'S e Corretoras de Valores", 'Investidor Institucional', "Invest Institucional Nacional", 'Invest Institucional Estrangeiro','Pessoa Jurídica Não Financeira', 'Pessoa Física', 'Total Geral']:
        for i in range(0, len(dados) - 10, 5):
            str_sql = "INSERT INTO bmf (data,tipo,compravenda,n_contratos) values (%s,%s,%s,%s)"
            cursor.execute(str_sql, (data_arquivo, dados[0 + i], 'C', dados[1 + i]))
            cursor.execute(str_sql, (data_arquivo, dados[0 + i], 'V', dados[3 + i]))

        conn.commit()
    elif dados[::5]  == ['Pessoa Jurídica Financeira', 'Bancos', "DTVM'S e Corretoras de Valores","Outras Jurídicas Financeiras",
                                      'Investidor Institucional', "Invest Institucional Nacional",
                                      'Invest Institucional Estrangeiro', 'Pessoa Jurídica Não Financeira',
                                      'Pessoa Física', 'Total Geral']:
        for i in range(0, len(dados) -5, 5):
            str_sql = "INSERT INTO bmf (data,tipo,compravenda,n_contratos) values (%s,%s,%s,%s)"
            cursor.execute(str_sql, (data_arquivo, dados[0 + i], 'C', dados[1 + i]))
            cursor.execute(str_sql, (data_arquivo, dados[0 + i], 'V', dados[3 + i]))

        conn.commit()

    elif dados[::5]  == ['Pessoa Jurídica Financeira', 'Bancos', "Outras Jurídicas Financeiras",'Investidor Institucional', "Invest Institucional Nacional", 'Investidores Não Residentes','Inv Não Residente - Res2689', 'Pessoa Jurídica Não Financeira', 'Pessoa Física','Total Geral']:
        for i in range(0, len(dados)-5, 5):
            str_sql = "INSERT INTO bmf (data,tipo,compravenda,n_contratos) values (%s,%s,%s,%s)"
            cursor.execute(str_sql, (data_arquivo, dados[0 + i], 'C', dados[1 + i]))
            cursor.execute(str_sql, (data_arquivo, dados[0 + i], 'V', dados[3 + i]))

        conn.commit()
    else:
        error('Houve mundanca no layout da pagina')


conn ,cursor,engine= conection("robos_b3")
lista = contexto(cursor,"bmf")



url = 'http://www2.bmf.com.br/pages/portal/bmfbovespa/lumis/lum-tipo-de-participante-ptBR.asp'

#for j in range(1,100000):

#ontem = datetime.datetime(int(lista[-1].split('-')[0]),int(lista[-1].split('-')[1]),int(lista[-1].split('-')[2])) + datetime.timedelta(-j)
#ontem = datetime.datetime(2004,3,16) + datetime.timedelta(-j)
#ontem = datetime.datetime.now() + datetime.timedelta(-2)
#if j in range(15,780,15):
#    print ontem
#    newidentity()


#r1 = requests.post(url,data = {'dData1' : "14/07/2020"})
r1 = requests.get(url)

soup = BeautifulSoup(r1.content, 'html.parser')

try:
    atualizado = soup.button.find_parent('div').find_next('div').get_text()
    if atualizado != '\n\n\n':
        caracteres = re.findall(r'(.*?)(..)/(..)/(....)(.*?)',atualizado)[0]
        data_arquivo = '-'.join(caracteres[3:0:-1])



        if data_arquivo not in lista:
            tabela = [x for x in soup.find_all('table') if x.caption.text.strip() == 'MERCADO FUTURO DE IBOVESPA'][0]
            if tabela.thead.find_all('th')[1].text.upper() != 'COMPRA' or tabela.thead.find_all('th')[2].text.upper() != 'VENDA' :
                error('erro na sequencia de colunas de compra e venda')
            dados = tabela.tbody.find_all('td')[0:50]
            dados = list(map(lambda x : x.text.strip().replace('.','').replace(',','.'),dados))
            parser(data_arquivo, dados)
            with open(r"checklist.txt", 'a') as checklist:
                checklist.writelines('bmf\n')

except:
    error('algum erro do processo em geral')