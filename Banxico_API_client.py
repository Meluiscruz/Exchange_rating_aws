import requests
import auth
import mysql_ops
import json
import http.client
import mimetypes
import ast
import pandas as pd
import numpy as np

from datetime import datetime
from time import sleep

#Prefijos y sufijos para el acceso a la API de Banxico.
BANXICO_PREFIX_BASE_OPORTUNO = 'https://www.banxico.org.mx/SieAPIRest/service/v1/series/'
#Drop exception
#BANXICO_PREFIX_BASE_OPORTUNO = 'https://www.banxico.org.mx/SieAPIRest/service/v1/ceries/'
BANXICO_SUFIX_BASE_OPORTUNO = '/datos/oportuno?token='
LIST_OF_BANXICO_SERIES = ['SF43787', 'SF43784', 'SF43788', 'SF43786']

def Banxico_oportuno(serie):
    url = BANXICO_PREFIX_BASE_OPORTUNO + str(serie) + BANXICO_SUFIX_BASE_OPORTUNO + auth.BANXICO_TOKEN
    try:
        answer = requests.get(url)
        if answer.status_code == 200:
            ex_rate = answer.json()['bmx']['series'][0]['datos'][0]['dato']
            m_date = datetime.now().strftime("%Y-%m-%d")
            m_time = datetime.now().strftime("%H:%M:%S")
            sleep(3)

            return {'serie':f'Tipo de cambio USD -> MXN {serie}', 'tipo de cambio (USD -> MXN)': ex_rate,
                    'fecha de lectura': m_date, 'hora de lectura': m_time}
        else:
            raise ValueError(f'Error: {answer.status_code}')
    except ValueError as ve:
        print(ve)
        #Exeption_1()

def run():

    list_of_banxico_dictionaries =[]
    #LIST_OF_BANXICO_SERIES = ['SF43787'check, 'SF43784'check, 'SF43788'check, 'SF43786'check]
    for serie in LIST_OF_BANXICO_SERIES:
        list_of_banxico_dictionaries.append(Banxico_oportuno(serie))
    mysql_ops.Banxico_Insertion_sf43787_buy_opening(list_of_banxico_dictionaries[0])
    mysql_ops.Banxico_Insertion_sf43784_sell_opening(list_of_banxico_dictionaries[1])
    mysql_ops.Banxico_Insertion_sf43788_buy_closing(list_of_banxico_dictionaries[2])
    mysql_ops.Banxico_Insertion_sf43786_sell_closing(list_of_banxico_dictionaries[3])

if __name__ == "__main__":
    run()