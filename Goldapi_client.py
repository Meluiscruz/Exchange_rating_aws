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

def run():

    gold_price = Metal_API_request(metal = 'XAU')
    mysql_ops.Metal_Insertion_gold(gold_price)
    silver_price = Metal_API_request(metal = 'XAG')
    mysql_ops.Metal_Insertion_silver(silver_price)

if __name__ == "__main__":
    run()