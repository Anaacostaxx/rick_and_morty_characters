#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  6 15:43:52 2023

@author: ana
"""

import pandas as pd
import requests
import json
from datetime import datetime

#Funcion para imprimir el objeto JSON y tener mejor visualización
def jprint(obj):
    #Crea una cadeda con formato del objeto JSON
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)
    
    
 
#Funcion para hacer la solicitud de consulta 'request' de los datos
def get_characters():
    #URL de la API RickAndMorty
    url = "https://rickandmortyapi.com/api/character"
    #Primera página de personajes
    page = 1
    #Arreglo para de personajes
    characters = []
    #Ciclo para recuperar todas las paginas donde se encuentran los datos de los personajes
    while page:
        # Hacer la solicitud a la API
        response = requests.get(url, params={'page': page})
        
        # Verificar el código de respuesta
        if response.status_code == 200:
            #obtener la respuesta de la API en formato json
            data = response.json()
            #Agregar los personajes de la página actual al total de personajes
            newCharacters = data["results"]
            characters.extend(newCharacters)
            
            # Pasar a la siguiente página si es que existe
            if data["info"]["next"]:
                page += 1
            else:
        
                page = None
        #Manda mensaje del error presentado en caso que la solicitud no haya sido exitosa
        else:
            print("Error: ", response.status_code)
            return []
    #Visualizacion de los datos de los personajes obtenidos
    #jprint(characters)
    return characters
    
# Función para extraer el año de una fecha
def extract_year_from_date(date_str):
    date_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%fZ')
    return date_obj.year




#Se llama la funcion para obtener los datos de los personajes
characters = get_characters()

#Los datos obtenidos se colocan en un data frame de pandas
df = pd.DataFrame(characters)
#print(df.shape)
#Se observan los nombres de las columnas del dataframe
#print(df.dtypes)

#crea un recuento de los datos faltantes por columna
#missing_values = df.isnull().sum()

# Imprimir el recuento de valores nulos en cada columna
#print(missing_values)



#Se extraen solamente los datos que se consideran relevantes  para el analisis de datos
df = df[["status", "species", "type", "gender", "location","created"]]

#Se obtiene solo el valor del nombre de la locacion, dejando de lado la url
df["location"] = df["location"].apply(lambda x: x["name"])
#Se obtiene solo el año de la fecha en que fue creado el personaje
df['created'] = df['created'].apply(extract_year_from_date)

# Reemplazar valores vacíos ('') del DataFrame por "Unknown"
df.replace('', 'unknown', inplace=True)

#Guardar el dataFrame en un archivo csv
df.to_csv('rick_and_morty_characters.csv', index=False)

#print(df)
