from extraer_datos import get_urls, descargar_csv
from rutas import crear_dir, DIR_BIBLIOTECAS, DIR_CINES, DIR_MUSEOS, CSV_BIBLIOTECAS, CSV_CINES, CSV_MUSEOS


if __name__ == '__main__':

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