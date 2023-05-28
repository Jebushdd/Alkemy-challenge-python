import pandas as pd

from rutas import CSV_BIBLIOTECAS, CSV_CINES, CSV_MUSEOS


def normalizar_campos(csv_file:str):
    # Leer csv
    raw_df = pd.read_csv(csv_file)
    # Normalizar campos y datos
    raw_df.columns = raw_df.columns.str.lower()
    raw_df.columns = raw_df.columns.str.normalize('NFKD').str.encode('ascii',errors='ignore').str.decode('utf-8')
    raw_df.fillna('s/d', inplace=True)
    return raw_df

def nuevos_campos(df:pd.DataFrame):
    match df.categoria[0]:
        case 'Salas de cine':
            df[['número de teléfono', 'mail']] = 's/d'
            new_df = df[['cod_localidad', 'id_provincia', 'id_departamento', 'categoria', 'provincia', 'localidad', 'nombre', 'direccion', 'cp', 'número de teléfono','mail' , 'web']]
        
        case 'Espacios de Exhibición Patrimonial':
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

def unir_dfs(lista_dfs:list):
    consolidado = pd.concat(lista_dfs, ignore_index=True)
    return consolidado


# Leer csvs y normalizar campos
raw_df_bibliotecas = normalizar_campos(CSV_BIBLIOTECAS)
raw_df_museos = normalizar_campos(CSV_MUSEOS)
raw_df_cines = normalizar_campos(CSV_CINES)
# Tomar campos requeridas en cada dataframe
df_bibliotecas = nuevos_campos(raw_df_bibliotecas)
df_museos = nuevos_campos(raw_df_museos)
df_cines = nuevos_campos(raw_df_cines)
# Crear dataframes con campos renombrados
df_bibliotecas = rename_cols(df_bibliotecas)
df_museos = rename_cols(df_museos)
df_cines = rename_cols(df_cines)
# Crear tabla unica
lista_dfs = [df_bibliotecas,df_museos,df_cines]
consolidado = unir_dfs(lista_dfs)




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