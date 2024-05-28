import mysql.connector

# Configuración de la conexión a la base de datos
config = {
    'user': 'root',  # tu usuario
    'password': 'Rubenmera_190508',  # tu contraseña
    'host': 'localhost',
    'database': 'tienda'
}

# Conectar a la base de datos
conn = mysql.connector.connect(**config)
cursor = conn.cursor()

# Obtener todas las tablas de la base de datos
cursor.execute("SHOW TABLES")
tables = cursor.fetchall()

def get_column_type(table_name, column_name):
    cursor.execute(f"SHOW COLUMNS FROM {table_name} LIKE '{column_name}'")
    column_info = cursor.fetchone()
    return column_info[1]  # El tipo de datos es el segundo elemento en el resultado de SHOW COLUMNS

def create_procedures(table_name, columns):
    primary_key = columns[0]
    insert_columns = ", ".join(columns[1:])
    insert_values = ", ".join([f"_{col}" for col in columns[1:]])
    update_set = ", ".join([f"{col} = _{col}" for col in columns[1:]])

    sql_procedures = f"""
    -- Procedimiento de INSERT para: {table_name}
    DELIMITER $$
    CREATE PROCEDURE Insert_{table_name} (
        {', '.join([f'IN _{col} {get_column_type(table_name, col)}' for col in columns[1:]])}
    )
    BEGIN
        INSERT INTO {table_name} ({insert_columns})
        VALUES ({insert_values});
    END$$
    DELIMITER ;

    -- Procedimiento SELECT para: {table_name}
    DELIMITER $$
    CREATE PROCEDURE Select_{table_name}()
    BEGIN
        SELECT * FROM {table_name};
    END$$
    DELIMITER ;

    -- Procedimiento de UPDATE para: {table_name}
    DELIMITER $$
    CREATE PROCEDURE Update_{table_name}(
        IN _{primary_key} INT, 
        {', '.join([f'IN _{col} {get_column_type(table_name, col)}' for col in columns[1:]])}
    )
    BEGIN
        UPDATE {table_name}
        SET {update_set}
        WHERE {primary_key} = _{primary_key};
    END$$
    DELIMITER ;

    -- Procedimiento de DELETE para: {table_name}
    DELIMITER $$
    CREATE PROCEDURE Delete_{table_name}(IN _{primary_key} INT)
    BEGIN
        DELETE FROM {table_name}
        WHERE {primary_key} = _{primary_key};
    END$$
    DELIMITER ;
    """
    return sql_procedures

sql_script = ""
for (table_name,) in tables:
    cursor.execute(f"SHOW COLUMNS FROM {table_name}")
    columns = [column[0] for column in cursor.fetchall()]
    sql_script += create_procedures(table_name, columns)

# Escribe el script a un archivo
with open("crud_procedures.sql", "w") as file:
    file.write(sql_script)

# Cierra la conexión
cursor.close()
conn.close()

print("Script SQL generado exitosamente.")
