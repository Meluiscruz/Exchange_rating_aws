import requests
import auth
import json
import http.client
import mimetypes

from datetime import datetime
from time import sleep

#Consulta de tipo de cambio desde FIXER IO.
FIXER_URL_BASE = 'http://data.fixer.io/api/latest?access_key='
DEFAULT_BASE = '&base=EUR'

#Prefijos y sufijos para el acceso a la API de Banxico.
BANXICO_PREFIX_BASE_OPORTUNO = 'https://www.banxico.org.mx/SieAPIRest/service/v1/series/'
BANXICO_SUFIX_BASE_OPORTUNO = '/datos/oportuno?token='

#Prefijos y sufijos para el acceso a la API de GoldAPI
GOLD_API_URL_BASE = 'www.goldapi.io'

def Gold_API_request():

    try:
        conn = http.client.HTTPSConnection(GOLD_API_URL_BASE)
        playload = ''
        headers = {'x-access-token': auth.GOLD_API_KEY, 'Content-Type': 'application/json'}
        f_date = datetime.now().strftime("%Y%m%d")
        conn.request("GET",f"/api/XAU/USD/{f_date}", playload, headers)
        res = conn.getresponse()

        if res.status == 200:
            data = res.read()

            return data.decode("utf-8")
        else:
            raise ValueError(f'Error: {res.status}')
    except ValueError as ve:
        print(ve)
        #Exeption_1()

def Banxico_oportuno(serie):
    url = BANXICO_PREFIX_BASE_OPORTUNO + str(serie) + BANXICO_SUFIX_BASE_OPORTUNO + auth.BANXICO_TOKEN
    try:
        answer = requests.get(url)
        if answer.status_code == 200:
            ex_rate = answer.json()['bmx']['series'][0]['datos'][0]['dato']
            m_date = datetime.now().strftime("%Y-%m-%d")
            m_time = datetime.now().strftime("%H:%M:%S")
            sleep(3)

            return {'serie':serie, 'tipo de cambio': ex_rate, 'fecha de lectura': m_date, 'hora de lectura': m_time}
        else:
            raise ValueError(f'Error: {answer.status_code}')
    except ValueError as ve:
        print(ve)
        #Exeption_1()

def Fixer_io( ): #Función que me permite tomar el tipo de cambio de una fuente externa a Banxico.
    url = FIXER_URL_BASE + auth.FIXER_API_KEY + DEFAULT_BASE
    answer = requests.get(url)
    return answer

def run():

    dollar_buy_opening = Banxico_oportuno(serie = 'SF43787')
    #print(dollar_buy_opening)
    dollar_sell_opening = Banxico_oportuno(serie = 'SF43784')
    dollar_buy_closing = Banxico_oportuno(serie = 'SF43788')
    dollar_sell_closing = Banxico_oportuno(serie = 'SF43786')
    gold_price = Gold_API_request()
    print(gold_price)

    #dollar_mxn_from_fixer = Fixer_io( ) #El argumento de la función será la divisa.

if __name__ == "__main__":
    run()