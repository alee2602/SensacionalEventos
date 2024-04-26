# conexion.py
import psycopg2
from psycopg2 import Error

def crear_conexion():
    try:
        # Conexión a la base de datos PostgreSQL
        conexion = psycopg2.connect(
            user="postgres",
            password="pelu1503",
            host="localhost",
            port="5432",
            database="sensacionaleventosdb"
        )
        return conexion
    except (Exception, Error) as error:
        print("Error al conectarse a la base de datos:", error)

def ejecutar_script(conexion, script_file):
    try:
        # Abre el archivo del script y ejecuta las declaraciones SQL
        with open(script_file, 'r') as file:
            script = file.read()
            cursor = conexion.cursor()
            cursor.execute(script)
            conexion.commit()
            print("Script ejecutado correctamente.")
    except (Exception, Error) as error:
        print("Error al ejecutar el script:", error)
    finally:
        if conexion:
            cursor.close()
            conexion.close()
            print("Conexion cerrada.")

def verificar_credenciales(username, password):
    try:
        conexion=crear_conexion()
        cursor = conexion.cursor()

        # Consulta para verificar las credenciales del usuario
        query = "SELECT * FROM usuarios WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        usuario = cursor.fetchone()

        cursor.close()
        conexion.close()

        return usuario

    except (Exception, Error) as error:
        print("Error al verificar las credenciales:", error)
        return None

if __name__ == "__main__":
    conexion = crear_conexion()
    if conexion:
        ejecutar_script(conexion, "db/schema.sql")
