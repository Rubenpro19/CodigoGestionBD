import mysql.connector
from mysql.connector import Error
import subprocess
import time
import json
import tkinter as tk 
from tkinter import filedialog
import os

def cargar_configuracion(ruta_archivo):
    with open(ruta_archivo, 'r') as archivo:
        return json.load(archivo)

ruta_archivo = r'C:\Users\RUBEN\OneDrive - ULEAM\NIVELACIÓN (CUARTO-QUINTO)\Gestion de Base de Datos\codigo\Seguridad\config.json'

configuracion = cargar_configuracion(ruta_archivo)

DB_HOST = configuracion['DB_HOST']
DB_PORT = configuracion['DB_PORT']
DB_NAME = configuracion['DB_NAME']
DB_USER = configuracion['DB_USER']
DB_PASSWORD = configuracion['DB_PASSWORD']

def conectar_base_datos():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f'Error conectando a la base de datos: {e}')
        return None

def consultar_usuarios():
    connection = conectar_base_datos()
    if connection:
        cursor = None
        try:
            cursor = connection.cursor()

            sql_consultar_usuarios = "SELECT user FROM mysql.user;"
            cursor.execute(sql_consultar_usuarios)
            resultados = cursor.fetchall()

            print("Lista de usuarios:")
            for fila in resultados:
                usuario = fila
                print(f"Usuario: {usuario}")

        except Error as e:
            print(f'Error ejecutando la consulta: {e}')

        finally:
            if cursor:
                cursor.close()
            connection.close()
            #print('Conexión a la base de datos cerrada')

def crear_usuario():
    nombre = input("Ingrese el nombre del nuevo usuario: ")
    clave = input("Ingrese la contraseña para el nuevo usuario: ")

    connection = conectar_base_datos()
    if connection:
        cursor = None
        try:
            cursor = connection.cursor()

            sql_crear_usuario = f"CREATE USER '{nombre}'@'localhost' IDENTIFIED BY '{clave}';"

            cursor.execute(sql_crear_usuario)
            connection.commit()

            print(f"Usuario '{nombre}' creado exitosamente.")

        except Error as e:
            print(f'Error ejecutando la consulta: {e}')

        finally:
            if cursor:
                cursor.close()
            connection.close()
            #print('Conexión a la base de datos cerrada')

def modificar_usuario():
    print('Estos son los usuarios existentes:')
    consultar_usuarios()
    nombre = input("Ingrese el nombre del usuario que desea modificar: ")
    nueva_clave = input("Ingrese la nueva contraseña para el usuario: ")

    connection = conectar_base_datos()
    if connection:
        cursor = None
        try:
            cursor = connection.cursor()

            sql_modificar_usuario = f"ALTER USER '{nombre}'@'localhost' IDENTIFIED BY '{nueva_clave}';"

            cursor.execute(sql_modificar_usuario)
            connection.commit()

            print(f"Contraseña del usuario '{nombre}' modificada exitosamente.")

        except Error as e:
            print(f'Error ejecutando la consulta: {e}')

        finally:
            if cursor:
                cursor.close()
            connection.close()
            #print('Conexión a la base de datos cerrada')

def eliminar_usuario():
    consultar_usuarios()
    nombre = input("Ingrese el nombre del usuario que desea eliminar: ")

    connection = conectar_base_datos()
    if connection:
        cursor = None
        try:
            cursor = connection.cursor()

            sql_eliminar_usuario = f"DROP USER '{nombre}'@'localhost';"

            cursor.execute(sql_eliminar_usuario)
            connection.commit()

            print(f"Usuario '{nombre}' eliminado exitosamente.")

        except Error as e:
            print(f'Error ejecutando la consulta: {e}')

        finally:
            if cursor:
                cursor.close()
            connection.close()
            #print('Conexión a la base de datos cerrada')

def crear_rol():
    nombre_rol = input("Ingrese el nombre del rol que desea crear: ")
    permisos = input("Ingrese los permisos del rol separados por comas (Ejemplo: SELECT,INSERT,UPDATE,DELETE,CREATE,DROP,ETC): ")

    connection = conectar_base_datos()
    if connection:
        cursor = None
        try:
            cursor = connection.cursor()

            # Define los permisos como una lista
            permisos = permisos.split(',')

            # Define el comando SQL para crear el rol
            sql_crear_rol = f"CREATE ROLE {nombre_rol};"

            cursor.execute(sql_crear_rol)
            connection.commit()

            # Otorga los permisos al rol
            for permiso in permisos:
                cursor.execute(f"GRANT {permiso.strip()} ON prueba.* TO {nombre_rol};")
                connection.commit()

            print(f"Rol '{nombre_rol}' creado exitosamente con los siguientes permisos: {permisos}")

        except Error as e:
            print(f'Error ejecutando la consulta: {e}')

        finally:
            if cursor:
                cursor.close()
            connection.close()
            print('Conexión a la base de datos cerrada')

def ver_roles():

    connection = conectar_base_datos()
    if connection:
        cursor = None
        try:
            cursor = connection.cursor()

            # Define el comando SQL para obtener los roles
            sql_ver_roles = "SELECT DISTINCT User FROM mysql.user WHERE User != '' AND Host = '%';"

            cursor.execute(sql_ver_roles)

            # Obtén los resultados de la consulta
            resultados = cursor.fetchall()

            # Imprime los roles
            print("Lista de roles:")
            for fila in resultados:
                print(f"Rol: {fila[0]}")

        except Error as e:
            print(f'Error ejecutando la consulta: {e}')

        finally:
            if cursor:
                cursor.close()
            connection.close()
            print('Conexión a la base de datos cerrada')

def eliminar_rol():
    ver_roles()
    nombre_rol = input("Ingrese el nombre del rol que desea eliminar: ")

    connection = conectar_base_datos()
    if connection:
        cursor = None
        try:
            cursor = connection.cursor()

            # Define el comando SQL para eliminar el rol
            sql_eliminar_rol = f"DROP ROLE IF EXISTS {nombre_rol};"

            cursor.execute(sql_eliminar_rol)
            connection.commit()

            print(f"Rol '{nombre_rol}' eliminado exitosamente.")

        except Error as e:
            print(f'Error ejecutando la consulta: {e}')

        finally:
            if cursor:
                cursor.close()
            connection.close()
            print('Conexión a la base de datos cerrada')

def asignar_rol():
    usuario = input("Ingrese el nombre de usuario al que desea asignar el rol: ")
    rol = input("Ingrese el nombre del rol que desea asignar: ")

    connection = conectar_base_datos()
    if connection:
        cursor = None
        try:
            cursor = connection.cursor()

            # Define el comando SQL para asignar el rol al usuario
            sql_asignar_rol = f"GRANT {rol} TO '{usuario}'@'localhost';"

            cursor.execute(sql_asignar_rol)
            connection.commit()

            print(f"Rol '{rol}' asignado exitosamente al usuario '{usuario}'.")

        except Error as e:
            print(f'Error ejecutando la consulta: {e}')

        finally:
            if cursor:
                cursor.close()
            connection.close()
            #print('Conexión a la base de datos cerrada')

def mostrar_bases_datos(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SHOW DATABASES")
        bases_datos = cursor.fetchall()
        print("Bases de datos disponibles:")
        for bd in bases_datos:
            print(bd[0])

    except Error as e:
        print(f"Error al mostrar las bases de datos: {e}")

def seleccionar_carpeta():
    root = tk.Tk()
    root.withdraw()
    carpeta_destino = filedialog.askdirectory(title="Selecciona la carpeta de destino para el respaldo")
    root.destroy()
    return carpeta_destino

def seleccionar_archivo():
    root = tk.Tk()
    root.withdraw()
    archivo_respaldo = filedialog.askopenfilename(title="Selecciona el archivo de respaldo")
    root.destroy()
    return archivo_respaldo

def hacer_respaldo():

    try:
        connection = conectar_base_datos()

        if connection:
            mostrar_bases_datos(connection)
            nombre_base_datos = input("Ingrese el nombre de la base de datos que desea respaldar: ")
            # Verificar si la base de datos existe
            cursor = connection.cursor()
            cursor.execute(f"USE {nombre_base_datos}")
            for _ in cursor:
                pass  # Leer todos los resultados de la consulta
            cursor.close()
            # Obtener la fecha y hora actual para agregar al nombre del archivo de respaldo
            fecha_hora_actual = time.strftime("%Y-%m-%d_%H-%M-%S")

            # Crear una instancia de Tkinter y ocultar la ventana principal
            carpeta_destino = seleccionar_carpeta()

            if carpeta_destino:
                # Definir el nombre del archivo de respaldo
                nombre_archivo = f"{nombre_base_datos}_{fecha_hora_actual}.sql"
                ruta_respaldo = os.path.join(carpeta_destino, nombre_archivo)

                comando = f"mysqldump -u root -p -P 3307 {nombre_base_datos} > {ruta_respaldo}"
                # Ejecutar el comando en el shell
                proceso = subprocess.Popen(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                salida, errores = proceso.communicate()
        
                if proceso.returncode == 0:
                    print(f"Respaldo exitoso en: {ruta_respaldo}")
                else:
                    print(f"Error al hacer el respaldo: {errores.decode('utf-8')}")
            else:
                print("No se seleccionó ninguna carpeta. Respaldo cancelado.")
    except Error as e:
        print(f"Error al respaldar la base de datos: {e}")
        print("La base de datos especificada no se encuentra en el servidor MySQL.")
    finally:
        if connection.is_connected():
            connection.close()
            print("Conexión a MySQL cerrada.")

def restaurar_respaldo():
    try:
        connection = conectar_base_datos()

        if connection:
            nombre_nueva_base = input("Ingrese el nombre de la nueva base de datos: ")

            # Crear una nueva base de datos
            try:
                cursor = connection.cursor()
                cursor.execute(f"CREATE DATABASE {nombre_nueva_base}")
                print(f"Base de datos '{nombre_nueva_base}' creada exitosamente.")
            except Error as e:
                print(f"Error al crear la base de datos: {e}")
                return

            archivo_respaldo = seleccionar_archivo()
            if archivo_respaldo:
                comando = f"mysql -u root -p -P 3307 {nombre_nueva_base} < {archivo_respaldo}"
                # Ejecutar el comando en el shell
                proceso = subprocess.Popen(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                salida, errores = proceso.communicate()

                if proceso.returncode == 0:
                    print(f"Restauración exitosa en la base de datos: {nombre_nueva_base}")
                else:
                    print(f"Error al restaurar la base de datos: {errores.decode('utf-8')}")
            else:
                print("No se seleccionó ningún archivo de respaldo. Restauración cancelada.")
    except Error as e:
        print(f"Error al restaurar la base de datos: {e}")
    finally:
        if connection.is_connected():
            connection.close()
            print("Conexión a MySQL cerrada.")

def listar_entidades():
    try:
        connection = conectar_base_datos()

        if connection:
            cursor = connection.cursor()

            mostrar_bases_datos(connection)
            
            nombre_base_datos = input("Ingrese el nombre de la base de datos que desea consultar: ")

            # Verificar si la base de datos existe
            cursor.execute("SHOW DATABASES LIKE %s", (nombre_base_datos,))
            if cursor.fetchone():
                cursor.execute(f"USE {nombre_base_datos}")

                # Listar las tablas de la base de datos
                cursor.execute("SHOW TABLES")
                tablas = cursor.fetchall()
                if tablas:
                    print(f"Tablas en la base de datos '{nombre_base_datos}':")
                    for tabla in tablas:
                        print(f"- {tabla[0]}")
                else:
                    print(f"No se encontraron tablas en la base de datos '{nombre_base_datos}'.")
            else:
                print(f"La base de datos '{nombre_base_datos}' no existe.")
    except Error as e:
        print(f"Error al listar entidades de la base de datos: {e}")
    finally:
        if connection.is_connected():
            connection.close()
            #print("Conexión a MySQL cerrada.")

def listar_atributos():
    try:
        connection = conectar_base_datos()

        if connection:
            cursor = connection.cursor()

            mostrar_bases_datos(connection)
            
            nombre_base_datos = input("Ingrese el nombre de la base de datos que desea consultar: ")

            # Verificar si la base de datos existe
            cursor.execute("SHOW DATABASES LIKE %s", (nombre_base_datos,))
            if cursor.fetchone():
                cursor.execute(f"USE {nombre_base_datos}")

                # Listar las tablas de la base de datos
                cursor.execute("SHOW TABLES")
                tablas = cursor.fetchall()
                if tablas:
                    print(f"Entidades y atributos en la base de datos '{nombre_base_datos}':")
                    for tabla in tablas:
                        print(f"- Tabla: {tabla[0]}")
                        # Obtener información de esquema de la tabla
                        cursor.execute(f"DESCRIBE {tabla[0]}")
                        atributos = cursor.fetchall()
                        print("  Atributos:")
                        for atributo in atributos:
                            print(f"    - {atributo[0]}")  # Nombre del atributo
                else:
                    print(f"No se encontraron tablas en la base de datos '{nombre_base_datos}'.")
            else:
                print(f"La base de datos '{nombre_base_datos}' no existe.")
    except Error as e:
        print(f"Error al listar entidades de la base de datos: {e}")
    finally:
        if connection.is_connected():
            connection.close()
            #print("Conexión a MySQL cerrada.")

def agregar_entidad():
    try:
        connection = conectar_base_datos()

        if connection:
            cursor = connection.cursor()

            mostrar_bases_datos(connection)

            nombre_base_datos = input("Ingrese el nombre de la base de datos en la que desea agregar la entidad: ")
            cursor.execute("SHOW DATABASES")
            bases_datos = cursor.fetchall()
            if (nombre_base_datos,) in bases_datos:
                cursor.execute(f"USE {nombre_base_datos}")

                nombre_entidad = input("Ingrese el nombre de la nueva entidad: ")

                # Solicitar los nombres de los atributos y sus tipos de datos
                atributos = []
                while True:
                    nombre_atributo = input("Ingrese el nombre del atributo (o 'fin' para terminar): ")
                    if nombre_atributo.lower() == 'fin':
                        break
                    tipo_atributo = input(f"Ingrese el tipo de dato para '{nombre_atributo}': ")
                    atributos.append((nombre_atributo, tipo_atributo))

                # Crear la consulta para agregar la nueva entidad con sus atributos
                consulta = f"CREATE TABLE {nombre_entidad} (id_{nombre_entidad} INT AUTO_INCREMENT PRIMARY KEY,"
                for nombre, tipo in atributos:
                    consulta += f" {nombre} {tipo},"
                consulta = consulta.rstrip(',') + ")"
                
                # Ejecutar la consulta
                cursor.execute(consulta)
                print(f"Entidad '{nombre_entidad}' agregada exitosamente con sus atributos.")
            else:
                print(f"La base de datos '{nombre_base_datos}' no existe.")
    except Error as e:
        print(f"Error al agregar la entidad: {e}")
    finally:
        if connection.is_connected():
            connection.close()
            print("Conexión a MySQL cerrada.")

def main():
    while True:
        print("Seleccione una opción:")
        print("1. Consultar usuarios")
        print("2. Crear usuario")
        print("3. Modificar usuario")
        print("4. Eliminar usuario")
        print("5. Crear Rol")
        print("6. Ver Rol")
        print("7. Eliminar Rol")
        print("8. Asignar Rol")
        print("9. Crear Respaldo BD")
        print("10. Usar Respaldo")
        print("11. Listar Entidades")
        print("12. Listar Atributos")
        print("13. Agregar Entidad con Atributos")
        print("12. Salir")
        opcion = input("Ingrese el número de la opción que desea ejecutar: ")
        
        if opcion == '1':
            consultar_usuarios()
        elif opcion == '2':
            crear_usuario()
        elif opcion == '3':
            modificar_usuario()
        elif opcion == '4':
            eliminar_usuario()
        elif opcion == '5':
            crear_rol()
        elif opcion == '6':
            ver_roles()
        elif opcion == '7':
            eliminar_rol()
        elif opcion == '8':
            asignar_rol()
        elif opcion == '9':
            hacer_respaldo()
        elif opcion == '10':
            restaurar_respaldo()
        elif opcion == '11':
            listar_entidades()
        elif opcion == '12':
            print("Saliendo del programa...")
            break
        else:
            print("Opción inválida. Por favor, ingrese un número válido.")


def listar_entidades2(base_datos):
    cursor = base_datos.cursor()
    cursor.execute("SHOW TABLES")
    tablas = cursor.fetchall()
    print("Entidades disponibles:")
    for tabla in tablas:
        print(f"- {tabla[0]}")

def mostrar_datos(base_datos, entidad, atributos):
    cursor = base_datos.cursor()
    consulta = f"SELECT {', '.join(atributos)} FROM {entidad}"
    cursor.execute(consulta)
    datos = cursor.fetchall()
    print(f"\nDatos de la entidad '{entidad}':")
    for dato in datos:
        print(", ".join(str(d) for d in dato))

def generar_reporte():

    try:
        connection = conectar_base_datos()

        if connection:
            cursor = connection.cursor()

            # Mostrar las bases de datos disponibles
            cursor.execute("SHOW DATABASES")
            bases_datos = cursor.fetchall()
            print("Bases de datos disponibles:")
            for db in bases_datos:
                print(f"- {db[0]}")
            
            nombre_base_datos = input("Ingrese el nombre de la base de datos que desea consultar: ")

            # Verificar si la base de datos existe
            cursor.execute("SHOW DATABASES LIKE %s", (nombre_base_datos,))
            if cursor.fetchone():
                cursor.execute(f"USE {nombre_base_datos}")

                while True:
                    listar_entidades2(connection)
                    entidad = input("\nIngrese el nombre de la entidad que desea consultar (o 'fin' para salir): ")
                    if entidad.lower() == 'fin':
                        break
                    if (entidad,) in cursor.fetchall():
                        cursor.execute(f"DESCRIBE {entidad}")
                        atributos = [atributo[0] for atributo in cursor.fetchall()]
                        print("Atributos disponibles:")
                        print(", ".join(atributos))
                        seleccionados = input("Ingrese los nombres de los atributos separados por comas (o '*' para todos): ")
                        if seleccionados.strip() == '*':
                            atributos_seleccionados = atributos
                        else:
                            atributos_seleccionados = [a.strip() for a in seleccionados.split(",")]
                        mostrar_datos(connection, entidad, atributos_seleccionados)
                    else:
                        print(f"La entidad '{entidad}' no existe en la base de datos.")
            else:
                print(f"La base de datos '{nombre_base_datos}' no existe.")
    except Error as e:
        print(f"Error al generar el reporte: {e}")
    finally:
        if connection.is_connected():

            connection.close()
            print("Conexión a MySQL cerrada.")

generar_reporte()