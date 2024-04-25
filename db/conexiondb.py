# conexion.py
import psycopg2
from psycopg2 import Error

def crear_conexion():
    try:
        # Conexión a la base de datos PostgreSQL
        conexion = psycopg2.connect(
            user="postgres",
            password="",
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

if __name__ == "__main__":
    conexion = crear_conexion()
    if conexion:
        ejecutar_script(conexion, "db/schema.sql")
