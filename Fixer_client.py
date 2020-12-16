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

def Turn_str_into_dic( word ):
    return ast.literal_eval(word)

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

    eur_dollar_from_Fixer = Fixer_io()
    mysql_ops.EUR_USD_Insertion(eur_dollar_from_Fixer)

if __name__ == "__main__":
    run()