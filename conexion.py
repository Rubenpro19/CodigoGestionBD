import json

def cargar_configuracion(ruta_archivo):
    with open(ruta_archivo, 'r') as archivo:
        return json.load(archivo)

# Obtén la ruta del archivo de configuración
ruta_archivo = r'C:\Users\RUBEN\OneDrive - ULEAM\NIVELACIÓN (CUARTO-QUINTO)\Gestion de Base de Datos\codigo\config.json'

# Cargar la configuración desde el archivo config.json
configuracion = cargar_configuracion(ruta_archivo)

# Obtener los valores necesarios de la configuración
DB_HOST = configuracion['DB_HOST']
DB_PORT = configuracion['DB_PORT']
DB_NAME = configuracion['DB_NAME']
DB_USER = configuracion['DB_USER']
DB_PASSWORD = configuracion['DB_PASSWORD']

