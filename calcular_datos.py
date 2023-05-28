
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