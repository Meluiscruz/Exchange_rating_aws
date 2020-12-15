import pymysql.cursors
import auth
import pandas as pd
import numpy as np

#LIST_OF_BANXICO_SERIES = ['SF43787'check, 'SF43784'check, 'SF43788'check, 'SF43786']

def Banxico_Insertion_sf43787_buy_opening ( dictionary ):
    
    connection = pymysql.connect(host = 'localhost', user = auth.MY_SQL_USER, password = auth.MY_SQL_PASSWORD, 
        db = 'tipos_de_cambio', charset = 'utf8mb4', cursorclass = pymysql.cursors.DictCursor)
    
    exchange_USD_MXN = dictionary['tipo de cambio (USD -> MXN)']
    measure_date = dictionary['fecha de lectura']
    measure_time = dictionary['hora de lectura']

    try:

        with connection.cursor() as cursor: 

            sql = "INSERT INTO `serie_sf43787_buy_opening`( `exchange_USD_MXN`, `measure_date`, `measure_time`) VALUES ('"+ exchange_USD_MXN +"','"+ measure_date +"', '"+ measure_time +"')"
            cursor.execute(sql)
            connection.commit()

    except Exception as E :

        print(E)

    finally:
        print('\nBanxico Insertion SF43787 is ok. Everything in its right place')
        connection.close()   

def Banxico_Insertion_sf43784_sell_opening ( dictionary ):
    
    connection = pymysql.connect(host = 'localhost', user = auth.MY_SQL_USER, password = auth.MY_SQL_PASSWORD, 
        db = 'tipos_de_cambio', charset = 'utf8mb4', cursorclass = pymysql.cursors.DictCursor)
    
    exchange_USD_MXN = dictionary['tipo de cambio (USD -> MXN)']
    measure_date = dictionary['fecha de lectura']
    measure_time = dictionary['hora de lectura']

    try:

        with connection.cursor() as cursor: 

            sql = "INSERT INTO `serie_sf43784_sell_opening`( `exchange_USD_MXN`, `measure_date`, `measure_time`) VALUES ('"+ exchange_USD_MXN +"', '"+ measure_date +"', '"+ measure_time +"')"
            cursor.execute(sql)
            connection.commit()

    except Exception as E :

        print(E)

    finally:
        print('\nBanxico Insertion SF43784 is ok. Everything in its right place')
        connection.close()

def Banxico_Insertion_sf43788_buy_closing ( dictionary ):
    
    connection = pymysql.connect(host = 'localhost', user = auth.MY_SQL_USER, password = auth.MY_SQL_PASSWORD, 
        db = 'tipos_de_cambio', charset = 'utf8mb4', cursorclass = pymysql.cursors.DictCursor)
    
    exchange_USD_MXN = dictionary['tipo de cambio (USD -> MXN)']
    measure_date = dictionary['fecha de lectura']
    measure_time = dictionary['hora de lectura']

    try:

        with connection.cursor() as cursor: 

            sql = "INSERT INTO `serie_sf43788_buy_closing`( `exchange_USD_MXN`, `measure_date`, `measure_time`) VALUES ('"+ exchange_USD_MXN +"', '"+ measure_date +"', '"+ measure_time +"')"
            cursor.execute(sql)
            connection.commit()

    except Exception as E :

        print(E)

    finally:
        print('\nBanxico Insertion SF43788 is ok. Everything in its right place')
        connection.close()

def Banxico_Insertion_sf43786_sell_closing ( dictionary ):
    
    connection = pymysql.connect(host = 'localhost', user = auth.MY_SQL_USER, password = auth.MY_SQL_PASSWORD, 
        db = 'tipos_de_cambio', charset = 'utf8mb4', cursorclass = pymysql.cursors.DictCursor)
    
    exchange_USD_MXN = dictionary['tipo de cambio (USD -> MXN)']
    measure_date = dictionary['fecha de lectura']
    measure_time = dictionary['hora de lectura']

    try:

        with connection.cursor() as cursor: 

            sql = "INSERT INTO `serie_sf43786_sell_closing`( `exchange_USD_MXN`, `measure_date`, `measure_time`) VALUES ('"+ exchange_USD_MXN +"', '"+ measure_date +"', '"+ measure_time +"')"
            cursor.execute(sql)
            connection.commit()

    except Exception as E :

        print(E)

    finally:
        print('\nBanxico Insertion SF43786 is ok. Everything in its right place')
        connection.close()

def Metal_Insertion_gold ( dictionary ):
    
    connection = pymysql.connect(host = 'localhost', user = auth.MY_SQL_USER, password = auth.MY_SQL_PASSWORD, 
        db = 'tipos_de_cambio', charset = 'utf8mb4', cursorclass = pymysql.cursors.DictCursor)
    
    metal_oz_to_USD = dictionary['tipo de cambio (USD/Oz)']
    measure_date = dictionary['fecha de lectura']
    measure_time = dictionary['hora de lectura']

    try:

        with connection.cursor() as cursor: 

            sql = "INSERT INTO `gold_usd_per_oz`( `metal_oz_to_USD`, `measure_date`, `measure_time`) VALUES ('"+ metal_oz_to_USD +"','"+ measure_date +"', '"+ measure_time +"')"
            cursor.execute(sql)
            connection.commit()

    except Exception as E :

        print(E)

    finally:
        print('\nGold price insertion is ok. Everything in its right place')
        connection.close()

def Metal_Insertion_silver ( dictionary ):
    
    connection = pymysql.connect(host = 'localhost', user = auth.MY_SQL_USER, password = auth.MY_SQL_PASSWORD, 
        db = 'tipos_de_cambio', charset = 'utf8mb4', cursorclass = pymysql.cursors.DictCursor)
    
    metal_oz_to_USD = dictionary['tipo de cambio (USD/Oz)']
    measure_date = dictionary['fecha de lectura']
    measure_time = dictionary['hora de lectura']

    try:

        with connection.cursor() as cursor: 

            sql = "INSERT INTO `silver_usd_per_oz`( `metal_oz_to_USD`, `measure_date`, `measure_time`) VALUES ('"+ metal_oz_to_USD +"','"+ measure_date +"', '"+ measure_time +"')"
            cursor.execute(sql)
            connection.commit()

    except Exception as E :

        print(E)

    finally:
        print('\nSilver price insertion is ok. Everything in its right place')
        connection.close()

def EUR_USD_Insertion ( dictionary ):
    
    connection = pymysql.connect(host = 'localhost', user = auth.MY_SQL_USER, password = auth.MY_SQL_PASSWORD, 
        db = 'tipos_de_cambio', charset = 'utf8mb4', cursorclass = pymysql.cursors.DictCursor)
    
    ex_rate_EUR_MXN = dictionary['tipo de cambio (EUR -> MXN)']
    ex_rate_EUR_USD = dictionary['tipo de cambio (EUR -> USD)']
    measure_date = dictionary['fecha de lectura']
    measure_time = dictionary['hora de lectura']

    try:

        with connection.cursor() as cursor: 

            sql = "INSERT INTO `eur_usd_from_fixer`(`ex_rate_EUR_MXN`, `ex_rate_EUR_USD`, `measure_date`, `measure_time`) VALUES ('"+ex_rate_EUR_MXN+"', '"+ex_rate_EUR_USD+"', '"+measure_date+"', '"+measure_time+"')"
            cursor.execute(sql)
            connection.commit()

    except Exception as E :

        print(E)

    finally:
        print('\nEUR ->MXN and EUR -> USD insertions are ok. Everything in its right place')
        connection.close()
