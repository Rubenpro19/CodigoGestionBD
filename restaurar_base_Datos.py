import os
import tkinter as tk
from tkinter import filedialog

def obtener_ruta_archivo():
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal de tkinter
    ruta_archivo = filedialog.askopenfilename()  # Mostrar el diálogo de selección de archivos para obtener la ruta del archivo
    root.destroy()  # Cerrar la ventana principal de tkinter
    return ruta_archivo

def crear_nueva_base_datos():
    nombre_nueva_base_datos = input("Ingrese el nombre de la nueva base de datos que desea crear: ")
    # Aquí deberías agregar el código para crear la nueva base de datos utilizando el nombre proporcionado por el usuario
    return nombre_nueva_base_datos

def restaurar_base_datos():
    try:
        # Pedir al usuario el nombre de la nueva base de datos
        nombre_nueva_base_datos = crear_nueva_base_datos()

        # Pedir al usuario que elija el archivo de respaldo
        print("Seleccione el archivo de respaldo:")
        ruta_archivo_respaldo = obtener_ruta_archivo()

        # Definir el comando de restauración
        comando_restauracion = f"mysql --defaults-extra-file=\"C:\\Users\\RUBEN\\OneDrive - ULEAM\\NIVELACIÓN (CUARTO-QUINTO)\\Gestion de Base de Datos\\codigo\\.my.cnf\" \"{nombre_nueva_base_datos}\" < \"{ruta_archivo_respaldo}\""

        # Ejecutar el comando de restauración
        os.system(comando_restauracion)
        print("¡La base de datos ha sido restaurada exitosamente en la nueva base de datos!")
    
    except Exception as e:
        print(f"Error al restaurar la base de datos: {e}")

restaurar_base_datos()