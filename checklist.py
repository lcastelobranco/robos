import os
import datetime
from helper import *


agora = datetime.datetime.now()
con,cursor,engine = conection('robos_b3')

a = open(r"checklist.txt", 'r').readlines()

def rodar(name,delay_days=0,delay_hour = 0):
    #Fim de semana#
    if delay_days  > agora.weekday() :
        delay_days +=2
    ##Fim de semana##
    last_data = list(contexto(cursor, name))[0]
    year = int(last_data.split('-')[0])
    month = int(last_data.split('-')[1])
    day = int(last_data.split('-')[2])

    if agora > datetime.datetime(year,month,day,delay_hour) + datetime.timedelta(delay_days):
        try:
            if name+'\n' not in a:
                os.system("python "+name+".py")
        except:
            pass


rodar("ibov",delay_days=0,delay_hour = 1)
rodar("small",delay_days=0,delay_hour = 1)
rodar("util",delay_days=0,delay_hour = 1)
rodar("mlcx",delay_days=0,delay_hour = 1)
rodar("imob",delay_days=0,delay_hour = 1)
rodar("ivbx",delay_days=0,delay_hour = 1)
rodar("idiv",delay_days=0,delay_hour = 1)
rodar("ifix",delay_days=0,delay_hour = 1)
rodar("icon",delay_days=0,delay_hour = 1)
rodar("ifnc",delay_days=0,delay_hour = 1)

rodar("bovespa",delay_days=2,delay_hour = 12)
rodar("bmf",delay_days=1,delay_hour = 1)
rodar("btc",delay_days=1,delay_hour = 20)
rodar("emprestimosreg",delay_days=1,delay_hour = 20)

a = open(r"checklist.txt", 'r').readlines()

#'btc'\ atualiza toda manha inclusive sabado
#'emprestimosreg'\ atualiza toda manha inclusive sabado
#'bovespa'\ atualiza toda tarde de segunda a sexta
#'composicaoibov' e outros indices atualizam toda manha inclusive sabado
#'bmf' atualiza toda manha inclusive sabado

o_que_deveria_ter_funcionado = {'btc\n', 'emprestimosreg\n', 'bovespa\n', 'bmf\n', 'ibov\n', 'small\n', 'util\n', 'mlcx\n', 'imob\n', 'ivbx\n', 'idiv\n', 'ifix\n', 'icon\n', 'ifnc\n'}
nao_precisava_funcionar = {'ptax\n', 'taxasreferenciais\n'}

if agora.hour == 22:
    if not(o_que_deveria_ter_funcionado.issubset(set(a))):
        send_sms("Algo deu errado em pegar os dados hoje do merc financeiro.\nFaltou esses:\n\n"+''.join(o_que_deveria_ter_funcionado - set(a)))

if agora.hour >= 23 and agora.weekday() not in (4,5):
#if agora.hour >= 23 and agora.weekday() not in (4,5):
    with open(r"checklist.txt", 'w') as checklist:
        checklist.write(''.join(nao_precisava_funcionar))