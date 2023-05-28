from bs4 import BeautifulSoup
import requests
import os
from datetime import date


def get_urls(url:str):
    '''
    Devuelve un diccionario con las urls de los recursos del dataset.
    Pasar como argumento la url del dataset.
    '''
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    diccionario = {}
    for i in soup.find_all('h3'):
        diccionario[i.text.strip()] = soup.find('h3', string=i.text)\
                             .find_previous('button', string='DESCARGAR')\
                             .find_previous('a')['href']
    return diccionario


def crear_str_dir(nombre_categoria:str):
    '''
    Devuelve el directorio donde se guarda el oputput.
    Toma como argumento un string con el nombre de la categoría del output.
    '''
    # Definir string año-mes
    anio_mes = date.today().strftime('%Y-%B').lower()
     
    # Definir directorio
    dir_actual = os.getcwd()
    dir_output = os.path.join(f'{dir_actual}/{nombre_categoria}/{anio_mes}')
    return dir_output


def crear_dir(dir_categoria:str):
    '''
    Crea el directorio con las rutas especificadas para cada categoria.
    Toma como argumento una ruta (dir_categoria).
    '''
    if not os.path.exists(dir_categoria):
            os.makedirs(dir_categoria)


def crear_dir_output(dir_categoria:str, nombre_categoria:str):
    '''
    Genera un string con la ruta del output en formato csv.
    Toma como argumento un string con el nombre de la categoría.
    '''
    dia_mes_anio = date.today().strftime('%d-%m-%Y')
    output_csv = os.path.join(f'{dir_categoria}/{nombre_categoria}-{dia_mes_anio}.csv')
    return output_csv


def descargar_csv(url_csv:str, dir_salida:str):
    '''
    Descarga el csv de la categoria correspondiente en la ruta especificada.
    Pasar como primer argumento la url al csv y como segundo argumento la ruta
    completa incluyendo el nombre del archivo de salida
    '''
    response = requests.get(url_csv)
    with open(dir_salida, 'wb') as csv:
        csv.write(response.content)

if __name__ == '__main__':

    # Definir URL principal y crear diccionario de URLs por base de datos
    url = 'https://datos.cultura.gob.ar/dataset/espacios-culturales-argentina-sinca'
    dataset = get_urls(url)

    # Tomar URL para cada base de datos
    url_bibliotecas = dataset.get('Bibliotecas Populares')
    url_museos = dataset.get('Museo')
    url_cines = dataset.get('Cine')

    # Definir rutas de los directorios para los outputs
    dir_bibliotecas = crear_str_dir('bibliotecas')
    dir_museos = crear_str_dir('museos')
    dir_cines = crear_str_dir('cines')

    # Crear directorios para los outputs
    crear_dir(dir_bibliotecas)
    crear_dir(dir_cines)
    crear_dir(dir_museos)

    # Definir rutas para los outputs
    csv_bibliotecas = crear_dir_output(dir_bibliotecas, 'bibliotecas')
    csv_museos = crear_dir_output(dir_museos, 'museos')
    csv_cines = crear_dir_output(dir_cines,'cines')

    # Descargar csvs
    descargar_csv(url_bibliotecas, csv_bibliotecas)
    descargar_csv(url_museos, csv_museos)
    descargar_csv(url_cines, csv_cines)