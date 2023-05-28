from bs4 import BeautifulSoup
import requests


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


def descargar_csv(url_csv:str, dir_salida:str):
    '''
    Descarga el csv de la categoria correspondiente en la ruta especificada.
    Pasar como primer argumento la url al csv y como segundo argumento la ruta
    completa incluyendo el nombre del archivo de salida
    '''
    response = requests.get(url_csv)
    with open(dir_salida, 'wb') as csv:
        csv.write(response.content)