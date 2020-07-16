#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import datetime
from helper import *


agora = datetime.datetime.now()
con,cursor,engine = conection('dados')

a = open(r"C:\Users\luiz\PycharmProjects\robos\checklist.txt", 'r').readlines()

def rodar(tipo_python,name,delay_days=0,delay_hour = 0):
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
                if   tipo_python == 2:
                    os.system("C:/Python27/python.exe C:/Users/luiz/PycharmProjects/robos/"+name+".py")
                elif tipo_python == 3:
                    os.system("python C:/Users/luiz/PycharmProjects/robos/"+name+".py")
                else:
                    print('Versao de python n existe')
        except:
            pass


rodar(2,"composicaoibov",delay_days=0,delay_hour = 1)
rodar(2,"bovespa",delay_days=2,delay_hour = 12)
rodar(2,"bmf",delay_days=1,delay_hour = 1)
rodar(3,"btc",delay_days=1,delay_hour = 20)
rodar(3,"emprestimosreg",delay_days=1,delay_hour = 20)

a = open(r"C:\Users\luiz\PycharmProjects\robos\checklist.txt", 'r').readlines()

#'btc'\ atualiza toda manha inclusive sabado
#'emprestimosreg'\ atualiza toda manha inclusive sabado
#'bovespa'\ atualiza toda tarde de segunda a sexta
#'composicaoibov' atualiza toda manha inclusive sabado
#'bmf' atualiza toda manha inclusive sabado

o_que_deveria_ter_funcionado = {'btc\n', 'emprestimosreg\n', 'bovespa\n', 'composicaoibov\n', 'bmf\n'}
nao_precisava_funcionar = {'ptax\n', 'taxasreferenciais\n'}

if agora.hour == 22:
    if not(o_que_deveria_ter_funcionado.issubset(set(a))):
        send_sms("Algo deu errado em pegar os dados hoje do merc financeiro.\nFaltou esses:\n\n"+''.join(o_que_deveria_ter_funcionado - set(a)))

if agora.hour >= 23 and agora.weekday() not in (4,5):
#if agora.hour >= 23 and agora.weekday() not in (4,5):
    with open(r"C:\Users\luiz\PycharmProjects\robos\checklist.txt", 'w') as checklist:
        checklist.write(''.join(nao_precisava_funcionar))