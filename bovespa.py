import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from helper import *
#import pdb


def parser(file_object,data_arquivo,hash):
    #pdb.set_trace()
    aux = [u'Investidores Individuais',u'Clubes de Investimento', u'Institucionais', u'Investidor Estrangeiro',u'Empresas Públicas e Privadas', u'Instituições Financeiras', u'Outros']
    #pdb.set_trace()
    if list(file_object.iloc[2:, 0]) == aux:
        if file_object.iloc[0,1].strip().upper() == 'COMPRAS' and file_object.iloc[0,4].strip().upper() == 'VENDAS' and file_object.iloc[1,1].strip().upper() == 'R$ MIL' and file_object.iloc[1,3].strip().upper() == 'R$ MIL':
            compras = list(pd.read_excel(r"temporarios\participacao.xls",skiprows=4,usecols= range(1,5),dtype=str).iloc[0:7,0])
            vendas =  list(pd.read_excel(r"temporarios\participacao.xls",skiprows=4,usecols= range(1,5),dtype=str).iloc[0:7,2])
            tipos = [u'Inv Individuais', u'Clubes de Inv', u'Institucional', u'Inves. Estrangeiro', u'Emp. Priv/Publ.', u'Instit. Financeiras',u'Outros']
            for i in tipos:
                str_sql = "INSERT INTO bovespa (data,tipo,compravenda,financeiro,hash) values (%s,%s,%s,%s,%s)"
                cursor.execute(str_sql, (data_arquivo, str(i), 'C', compras[tipos.index(i)],hash))
                cursor.execute(str_sql, (data_arquivo, str(i), 'V', vendas[tipos.index(i)],hash))
            #pdb.set_trace()
            conn.commit()
        else:
            error("algum erro no 'subheader' do arquivo")
    else:
        error('algum erro no header do arquivo')




conn ,cursor,engine= conection("robos_b3")
lista = contexto(cursor,"bovespa")
#print(sorted(list(set(lista))))


url = 'http://www.b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/consultas/mercado-a-vista/participacao-dos-investidores/volume-total/'
r1 = requests.get(url)
soup = BeautifulSoup(r1.content, 'html.parser')
e = soup.find_all(href=re.compile(r'/participacao'))[-1]['href']

hash = e.split('../')[-1]
#hash = ''
url =  'http://www.b3.com.br/'+hash
r2 = requests.get(url, allow_redirects=True)
open(r"temporarios\participacao.xls", 'wb').write(r2.content)

file_object = pd.read_excel(r"temporarios\participacao.xls",skiprows=2)
try:
    #data_arquivo ='-'.join(file_object.columns[0][-11:-1].split('/')[::-1])
    #data_arquivo = file_object.columns[1]
    #pdb.set_trace()
    data_arquivo = '-'.join(file_object.columns[0].split(' ')[-1].split('/')[::-1])
    
    
    
    if data_arquivo not in lista:
        parser(file_object,data_arquivo,hash)
        with open(r"checklist.txt", 'a') as checklist:
            checklist.writelines('bovespa\n')

except:
    error('algum erro do processo em geral')