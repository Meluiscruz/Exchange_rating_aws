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

#Consulta de tipo de cambio desde FIXER IO.
FIXER_URL_BASE = 'http://data.fixer.io/api/latest?access_key='
DEFAULT_BASE = '&base=EUR'

#Prefijos y sufijos para el acceso a la API de Banxico.
BANXICO_PREFIX_BASE_OPORTUNO = 'https://www.banxico.org.mx/SieAPIRest/service/v1/series/'
BANXICO_SUFIX_BASE_OPORTUNO = '/datos/oportuno?token='
LIST_OF_BANXICO_SERIES = ['SF43787', 'SF43784', 'SF43788', 'SF43786']

#Prefijos y sufijos para el acceso a la API de GoldAPI
GOLD_API_URL_BASE = 'www.goldapi.io'

def Turn_str_into_dic( word ):
    return ast.literal_eval(word)

def Metal_API_request(metal):

    try:
        conn = http.client.HTTPSConnection(GOLD_API_URL_BASE)
        playload = ''
        headers = {'x-access-token': auth.GOLD_API_KEY, 'Content-Type': 'application/json'}
        #f_date = datetime.now().strftime("%Y%m%d")
        f_date = "20201209" #Testing date
        conn.request("GET",f"/api/{metal}/USD/{f_date}", playload, headers)
        res = conn.getresponse()

        if res.status == 200:
            data = res.read()
            word = data.decode("utf-8")
            clean_dic = Turn_str_into_dic(word)

            if "error" in clean_dic:
                raise ValueError(f'Error: There was an error during extraction. Maybe there is no data available for this date or pair')
            else:
                price_in_usd = str(round(clean_dic['price'], 2))
                serie = metal
                m_date = datetime.now().strftime("%Y-%m-%d")
                m_time = datetime.now().strftime("%H:%M:%S")
                sleep(3)

                return {'serie': serie, 'tipo de cambio (USD/Oz)': price_in_usd, 
                        'fecha de lectura': m_date, 'hora de lectura': m_time}
        else:
            raise ValueError(f'Error: {conn.status_code}')
    
    except ValueError as ve:
        print(ve)
        #Exeption_2()
    finally:
        conn.close()

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

def Fixer_io( ): #Función que me permite tomar el tipo de cambio de una fuente externa a Banxico.
    url = FIXER_URL_BASE + auth.FIXER_API_KEY + DEFAULT_BASE
    try:

        answer = requests.get(url)
        if answer.status_code == 200:
            ex_rate_EUR_MXN = str(round(answer.json()['rates']['MXN'], 2))
            ex_rate_EUR_USD = str(round(answer.json()['rates']['USD'], 2))
            m_date = datetime.now().strftime("%Y-%m-%d")
            m_time = datetime.now().strftime("%H:%M:%S")
            sleep(3)

            return {'serie': 'Tipos de cambio EUR / USD', 'tipo de cambio (EUR -> MXN)': ex_rate_EUR_MXN,
                    'tipo de cambio (EUR -> USD)' : ex_rate_EUR_USD, 'fecha de lectura' : m_date,'hora de lectura': m_time}
        else:
            raise ValueError(f'Error: {answer.status_code}')
    except ValueError as ve:
        print(ve)
        #Exeption_3()

def run():

    list_of_banxico_dictionaries =[]
    #LIST_OF_BANXICO_SERIES = ['SF43787'check, 'SF43784'check, 'SF43788'check, 'SF43786'check]
    for serie in LIST_OF_BANXICO_SERIES:
        list_of_banxico_dictionaries.append(Banxico_oportuno(serie))
    mysql_ops.Banxico_Insertion_sf43787_buy_opening(list_of_banxico_dictionaries[0])
    mysql_ops.Banxico_Insertion_sf43784_sell_opening(list_of_banxico_dictionaries[1])
    mysql_ops.Banxico_Insertion_sf43788_buy_closing(list_of_banxico_dictionaries[2])
    mysql_ops.Banxico_Insertion_sf43786_sell_closing(list_of_banxico_dictionaries[3])

    eur_dollar_from_Fixer = Fixer_io()
    mysql_ops.EUR_USD_Insertion(eur_dollar_from_Fixer)

    gold_price = Metal_API_request(metal = 'XAU')
    mysql_ops.Metal_Insertion_gold(gold_price)
    silver_price = Metal_API_request(metal = 'XAG')
    mysql_ops.Metal_Insertion_silver(silver_price)

if __name__ == "__main__":
    run()