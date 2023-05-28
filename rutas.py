import os
from datetime import date


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

# Rutas constants

# Definir rutas de los directorios para los outputs
DIR_BIBLIOTECAS = crear_str_dir('bibliotecas')
DIR_MUSEOS = crear_str_dir('museos')
DIR_CINES = crear_str_dir('cines')

# Definir rutas para los outputs
CSV_BIBLIOTECAS = crear_dir_output(DIR_BIBLIOTECAS, 'bibliotecas')
CSV_MUSEOS = crear_dir_output(DIR_MUSEOS, 'museos')
CSV_CINES = crear_dir_output(DIR_CINES,'cines')