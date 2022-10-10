import pandas as pd
import os
from datetime import date

# ❕❕❕ Crear un constants para las strings de fechas y paths ❕❕❕

# Paths para csvs
# Definir strings de fechas
anio_mes = date.today().strftime('%Y-%B')
dia_mes_anio = date.today().strftime('%d-%m-%Y')

# Definir directorios
dir_actual = os.getcwd()
dir_bibliotecas = os.path.join(dir_actual+'/bibliotecas/'+anio_mes)
dir_museos = os.path.join(dir_actual+'/museos/'+anio_mes)
dir_cines = os.path.join(dir_actual+'/cines/'+anio_mes)

# Definir path de archivos descargados
csv_bibliotecas = os.path.join(dir_bibliotecas+'/bibliotecas-'+dia_mes_anio+'.csv')
csv_museos = os.path.join(dir_museos+'/museos-'+dia_mes_anio+'.csv')
csv_cines = os.path.join(dir_cines+'/cines-'+dia_mes_anio+'.csv')

# Leer csvs
raw_df_bibliotecas = pd.read_csv(csv_bibliotecas)
raw_df_museos = pd.read_csv(csv_museos)
raw_df_cines = pd.read_csv(csv_cines)

# Pre procesar nombres de variables
def set_columns_lower(df):
    '''
    Convierte los nombres de las variables
    del dataframe a minúsculas
    '''
    df.columns = df.columns.str.lower()

set_columns_lower(raw_df_bibliotecas)
set_columns_lower(raw_df_museos)
set_columns_lower(raw_df_cines)

# Crear lista de nomenclaturas para nueva tabla
columnas = ['cod_localidad', 'id_provincia', 'id_departamento', 'categoría', 
            'provincia', 'localidad', 'nombre', 'domicilio', 'código postal', 
            'número de teléfono', 'mail', 'web']

# Seleccionar columnas requeridas en cada dataframe
df_bibliotecas = raw_df_bibliotecas[['cod_loc', 'idprovincia', 'iddepartamento', 'categoría', 'provincia', 'localidad', 'nombre', 'domicilio', 'cp', 'teléfono', 'mail', 'web']]
df_museos = raw_df_museos[['cod_loc', 'idprovincia', 'iddepartamento', 'categoria', 'provincia', 'localidad', 'nombre', 'direccion', 'cp', 'telefono', 'mail', 'web']]

    # Museos necesita columnas para telefono y mail
raw_df_cines[['número de teléfono', 'mail']] = 's/d'
df_cines = raw_df_cines[['cod_localidad', 'id_provincia', 'id_departamento', 'categoria', 'provincia', 'localidad', 'nombre', 'direccion', 'cp', 'número de teléfono','mail' , 'web']]

# Renombrando columnas
def rename_cols(df, new_names):
    '''
    Crea un diccionario a partir de un zip entre las columnas actuales 
    del dataframe y una lista con sus correspondientes nuevos nombres
    Pasar como primer argumento el dataframe con las columnas a renombrar
    Pasar como segundo argumento la lista con los nuevos nombres de las columnas
    Los indices de ambos argumentos deben coincidir para que se descompaginen los nombres
    '''
    diccionario = dict(zip(df.columns, new_names))
    df = df.rename(columns=diccionario)
    return df

# Crear dataframes con columnas renombradas
df_bibliotecas = rename_cols(df_bibliotecas, columnas)
df_museos = rename_cols(df_museos, columnas)
df_cines = rename_cols(df_cines, columnas)

# Normalizando datos
df_bibliotecas.fillna('s/d', inplace=True)
df_museos.fillna('s/d', inplace=True)
df_cines.fillna('s/d', inplace=True)

# Crear tabla unica
consolidado = pd.concat([df_bibliotecas,df_museos,df_cines], ignore_index=True)

# Registros totales por categoria
registros_categoria = pd.DataFrame(consolidado.groupby(by= 'categoría')['categoría'].count())
registros_categoria.columns=['total_registros']

# Registros totales por fuente
registros_fuente = pd.concat([raw_df_bibliotecas,raw_df_museos,raw_df_cines], ignore_index=True)
registros_fuente = pd.DataFrame(registros_fuente.groupby(by='fuente')['fuente'].count())
registros_fuente.columns=['total_registros']

# Registros por provincia y categoria
registros_provincia_categoria = pd.DataFrame(consolidado.groupby(by=['provincia', 'categoría'])['provincia'].count())
registros_provincia_categoria.columns = ['total_registros']

# Tabla de cines
tabla_cines = raw_df_cines[['provincia', 'pantallas', 'butacas', 'espacio_incaa']].copy()
tabla_cines['espacio_incaa'] = (tabla_cines['espacio_incaa'] == 'Si').astype(int)
tabla_cines = tabla_cines.groupby(by='provincia').sum()