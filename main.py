from extraer_datos import get_urls, descargar_csv
from rutas import crear_dir, DIR_BIBLIOTECAS, DIR_CINES, DIR_MUSEOS, CSV_BIBLIOTECAS, CSV_CINES, CSV_MUSEOS
from transformar_datos import normalizar_csv, nuevos_campos, rename_cols, tabla_unificada, tabla_contador_registros, tabla_contador_cines


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
    raw_df_bibliotecas = normalizar_csv(CSV_BIBLIOTECAS)
    raw_df_museos = normalizar_csv(CSV_MUSEOS)
    raw_df_cines = normalizar_csv(CSV_CINES)

    # Tomar campos requeridos de cada dataframe
    df_bibliotecas = nuevos_campos(raw_df_bibliotecas)
    df_museos = nuevos_campos(raw_df_museos)
    df_cines = nuevos_campos(raw_df_cines)

    # Crear dataframes con columnas renombradas
    df_bibliotecas = rename_cols(df_bibliotecas)
    df_museos = rename_cols(df_museos)
    df_cines = rename_cols(df_cines)

    # Crear tabla unificada
    lista_dfs = [df_bibliotecas,df_museos,df_cines]
    consolidado = tabla_unificada(lista_dfs)
    
    # Crear tabla de contador general
    lista_raw_dfs = [raw_df_bibliotecas, raw_df_museos, raw_df_cines]
    contador_registros = tabla_contador_registros(lista_raw_dfs)
    
    # Crear tabla de contador para cines
    contador_cines = tabla_contador_cines(raw_df_cines)


    # -------- Test Parcial: Partes 1 y 2 -------- #
    # -------------------------------------------- #
    print('\n\ndf consolidado')
    print(consolidado)

    print('\n\ndf contador de registros')
    print(contador_registros)

    print('\n\ndf contador para cines')
    print(contador_cines)