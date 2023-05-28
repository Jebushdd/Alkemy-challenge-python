from extraer_datos import get_urls, descargar_csv
from rutas import crear_dir, DIR_BIBLIOTECAS, DIR_CINES, DIR_MUSEOS, CSV_BIBLIOTECAS, CSV_CINES, CSV_MUSEOS
from transformar_datos import normalizar_campos, nuevos_campos, rename_cols


if __name__ == '__main__':

    # -------- Parte 1: Extracción -------- #
    # ------------------------------------- #

    # Definir URL principal y crear diccionario de URLs por base de datos
    url = 'https://datos.cultura.gob.ar/dataset/espacios-culturales-argentina-sinca'
    dataset = get_urls(url)

    # Tomar URL para cada base de datos
    url_bibliotecas = dataset.get('Bibliotecas Populares')
    url_museos = dataset.get('Museo')
    url_cines = dataset.get('Cine')

    # Crear directorios para los outputs
    crear_dir(DIR_BIBLIOTECAS)
    crear_dir(DIR_CINES)
    crear_dir(DIR_MUSEOS)

    # Descargar csvs
    descargar_csv(url_bibliotecas, CSV_BIBLIOTECAS)
    descargar_csv(url_museos, CSV_MUSEOS)
    descargar_csv(url_cines, CSV_CINES)

    # -------- Parte 2: Transformación -------- #
    # ----------------------------------------- #

    # Cargar csvs y normalizar campos
    raw_df_bibliotecas = normalizar_campos(CSV_BIBLIOTECAS)
    raw_df_museos = normalizar_campos(CSV_MUSEOS)
    raw_df_cines = normalizar_campos(CSV_CINES)

    # Tomar campos requeridos de cada dataframe
    df_bibliotecas = nuevos_campos(raw_df_bibliotecas)
    df_museos = nuevos_campos(raw_df_museos)
    df_cines = nuevos_campos(raw_df_cines)

    # Crear dataframes con columnas renombradas
    df_bibliotecas = rename_cols(df_bibliotecas)
    df_museos = rename_cols(df_museos)
    df_cines = rename_cols(df_cines)
