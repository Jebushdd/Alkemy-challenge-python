from extraer_datos import get_urls, crear_str_dir, crear_dir, crear_dir_output, descargar_csv




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