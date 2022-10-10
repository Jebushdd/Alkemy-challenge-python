from bs4 import BeautifulSoup
import requests
import os
from datetime import date

url = 'https://datos.cultura.gob.ar/dataset/espacios-culturales-argentina-sinca'
r = requests.get(url)
contenido = r.text

soup = BeautifulSoup(r.text, 'lxml')

def get_urls(url):
    '''
    Devuelve un diccionario con las urls de los recursos del dataset
    Pasar como argumento la url del dataset
    '''
    diccionario = {}
    for i in soup.find_all('h3'):
        diccionario[i.text.strip()] = soup.find('h3', text=i.text)\
                             .find_previous('button', text='DESCARGAR')\
                             .find_previous('a')['href']
    return diccionario
dataset = get_urls(url)

# Definir strings de fechas
anio_mes = date.today().strftime('%Y-%B')
dia_mes_anio = date.today().strftime('%d-%m-%Y')

# Definir directorios
dir_actual = os.getcwd()
dir_bibliotecas = os.path.join(dir_actual+'/bibliotecas/'+anio_mes)
dir_museos = os.path.join(dir_actual+'/museos/'+anio_mes)
dir_cines = os.path.join(dir_actual+'/cines/'+anio_mes)

# Creando directorios
def crear_dir(dir_categoria):
    '''
    Crea el directorio con las rutas especificadas para cada categoria
    Pasar una ruta (dir_categoria) por vez
    '''
    if not os.path.exists(dir_categoria):
            os.makedirs(dir_categoria)

crear_dir(dir_bibliotecas)
crear_dir(dir_cines)
crear_dir(dir_museos)

# Definir urls para cada base de datos
url_bibliotecas = dataset.get('Bibliotecas Populares')
url_museos = dataset.get('Museo')
url_cines = dataset.get('Cine')

# Definir path para archivos descargados
csv_bibliotecas = os.path.join(dir_bibliotecas+'/bibliotecas-'+dia_mes_anio+'.csv')
csv_museos = os.path.join(dir_museos+'/museos-'+dia_mes_anio+'.csv')
csv_cines = os.path.join(dir_cines+'/cines-'+dia_mes_anio+'.csv')

# Descargando csvs
def descargar_csv(url_csv, dir_salida):
    '''
    Descarga el csv de la categoria correspondiente en la ruta especificada
    Pasar como primer argumento la url al csv y como segundo argumento la ruta
    completa incluyendo el nombre del archivo de salida
    '''
    response = requests.get(url_csv)
    with open(dir_salida, 'wb') as csv:
        csv.write(response.content)

descargar_csv(url_bibliotecas, csv_bibliotecas)
descargar_csv(url_museos, csv_museos)
descargar_csv(url_cines, csv_cines)