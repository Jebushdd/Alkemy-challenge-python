import unicodedata
import pandas as pd

from rutas import CSV_BIBLIOTECAS, CSV_CINES, CSV_MUSEOS


def normalizar_csv(csv_file:str):
    '''
    Carga un archivo csv como DataFrame y normaliza tanto sus campos
    como sus valores tipo string.
    Toma como argumento un string con la ruta al CSV
    '''
    # Leer csv
    raw_df = pd.read_csv(csv_file)
    # Normalizar campos
    raw_df.columns = raw_df.columns.str.lower()
    raw_df.columns = raw_df.columns.str.normalize('NFKD').str.encode('ascii',errors='ignore').str.decode('utf-8')
    
    # Normalizar datos
    raw_df = raw_df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    raw_df.fillna('s/d', inplace=True)

    def no_tildes(texto:str):
        '''
        Quita las tildes de un string. Toma como argumento un string.
        '''
        new_value = unicodedata.normalize('NFKD',texto).encode('ascii',errors='ignore').decode('utf-8')
        return new_value
    
    new_df = raw_df.applymap(lambda x: no_tildes(x) if isinstance(x, str) else x)
    
    # Unificar Tierra Del Fuego
    def limpiar_tdf(provincia:pd.Series):
        '''
        Quita el exceso de texto para 'Tierra del Fuego' en el campo 'Provincia'.
        Toma como argumento un objeto Pandas Series.
        '''
        return provincia.split(',')[0]

    new_df['provincia'] = new_df['provincia'].apply(limpiar_tdf)
    return new_df

def nuevos_campos(df:pd.DataFrame):
    match df.categoria[0]:
        case 'Salas de cine':
            new_df = df[['cod_localidad', 'id_provincia', 'id_departamento', 'categoria', 'provincia', 'localidad', 'nombre', 'direccion', 'cp']].copy()
            new_df[['número de teléfono', 'mail']] = 's/d'
            new_df['web'] = df['web']
        
        case 'Espacios de Exhibicion Patrimonial':
            new_df = df[['cod_loc', 'idprovincia', 'iddepartamento', 'categoria', 'provincia', 'localidad', 'nombre', 'direccion', 'cp', 'telefono', 'mail', 'web']]
        
        case 'Bibliotecas Populares':
            new_df = df[['cod_loc', 'idprovincia', 'iddepartamento', 'categoria', 'provincia', 'localidad', 'nombre', 'domicilio', 'cp', 'telefono', 'mail', 'web']]
    
    return new_df

def rename_cols(df:pd.DataFrame):
    '''
    Crea un diccionario a partir de un zip entre las columnas actuales 
    del dataframe y una lista con los correspondientes nuevos nombres.
    Pasar como argumento el dataframe con las columnas a renombrar.
    '''
    # Crear lista de campos para nueva tabla
    new_names = ['cod_localidad', 'id_provincia', 'id_departamento', 'categoría', 
                'provincia', 'localidad', 'nombre', 'domicilio', 'código postal', 
                'número de teléfono', 'mail', 'web']
    
    diccionario = dict(zip(df.columns, new_names))
    df = df.rename(columns=diccionario)
    return df

def tabla_unificada(lista_dfs:list):
    '''
    Concatena varios DataFrames y devuelve uno unificado. 
    Toma como argumento una lista de DataFrames.
    '''
    consolidado = pd.concat(lista_dfs, ignore_index=True)
    return consolidado

def tabla_contador_registros(lista_dfs:list):
    '''
    Concatena varios raw DataFrames y devuelve un unificado solo con 
    campos de provincia, fuente y categoría. 
    Toma como argumento una lista de DataFrames.
    '''
    contador_registros = pd.concat(lista_dfs, ignore_index=True)[['provincia','categoria','fuente']]
    return contador_registros

def tabla_contador_cines(df_cines:pd.DataFrame):
    '''
    Toma un raw DataFrame con la base de datos de Cines solo con los
    campos de Provincia, Cantidad de pantallas, Cantidad de butacas
    y Cantidad de espacios INCAA.
    Toma como argumento un DataFrame
    '''
    contador_cines = df_cines[['provincia','pantallas','butacas','espacio_incaa']]
    return contador_cines

def correr_script():
    # Leer csvs y normalizar campos
    raw_df_bibliotecas = normalizar_csv(CSV_BIBLIOTECAS)
    raw_df_museos = normalizar_csv(CSV_MUSEOS)
    raw_df_cines = normalizar_csv(CSV_CINES)
    # Tomar campos requeridas en cada dataframe
    df_bibliotecas = nuevos_campos(raw_df_bibliotecas)
    df_museos = nuevos_campos(raw_df_museos)
    df_cines = nuevos_campos(raw_df_cines)
    # Crear dataframes con campos renombrados
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

    return (consolidado,contador_registros,contador_cines)


if __name__ == '__main__':
    correr_script()