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
def insertar_producto(producto):
    try:
        conexion = crear_conexion()
        cursor = conexion.cursor()

        # Consulta para insertar un nuevo producto en el inventario
        query = "INSERT INTO inventario (producto, marca, valor, precio, cantidad, comentarios) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, producto)

        # Confirmar la transacción
        conexion.commit()

        return True

    except (Exception, Error) as error:
        print("Error al insertar el nuevo producto:", error)
        # Si ocurre algún error, se puede manejar aquí, y se puede devolver False o realizar alguna otra acción

    finally:
        # Cerrar el cursor y la conexión
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()

    return False  # Retornar False en caso de error para indicar que la operación no se completó con éxito

def editar_inventario(id, nuevos_datos):
    try:
        conexion = crear_conexion()
        cursor = conexion.cursor()
        print("88888888")
        print(id)
        print(nuevos_datos)
        print("88888888")

        # Consulta para actualizar los datos del inventario
        query = "UPDATE inventario SET producto = %s, marca = %s, valor = %s, precio = %s, cantidad = %s, comentarios = %s WHERE id = %s"
        cursor.execute(query, (nuevos_datos[0], nuevos_datos[1], nuevos_datos[2], nuevos_datos[3], nuevos_datos[4], nuevos_datos[5], id))

        # Confirmar la transacción
        conexion.commit()

    except Exception as e:
        # Manejar cualquier error que pueda ocurrir durante la edición del inventario
        print(f"Error al editar el inventario: {str(e)}")
        conexion.rollback()

    finally:
        # Cerrar el cursor y la conexión
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()
def eliminar_inventario(id):
    try:
        conexion = crear_conexion()
        cursor = conexion.cursor()

        # Consulta para eliminar un registro del inventario
        query = "DELETE FROM inventario WHERE id=%s"  # Usamos %s como marcador de posición para el valor del id
        cursor.execute(query, (id,))  # Pasamos el id como un solo elemento de una tupla

        # Confirmar la transacción
        conexion.commit()

        return True

    except (Exception, Error) as error:
        print("Error al eliminar el registro del inventario:", error)
        # Si ocurre algún error, se puede manejar aquí, y se puede devolver False o realizar alguna otra acción

    finally:
        # Cerrar el cursor y la conexión
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()

    return False  # Retornar False en caso de error para indicar que la operación no se completó con éxito


def obtener_inventario():
    try:
        conexion=crear_conexion()
        cursor = conexion.cursor()

        # Consulta para verificar las credenciales del usuario
        query = "SELECT * FROM inventario"
        cursor.execute(query)
        inventario = cursor.fetchall()

        cursor.close()
        conexion.close()

        return inventario

    except (Exception, Error) as error:
        print("Error al verificar las credenciales:", error)
        return None

if __name__ == "__main__":
    conexion = crear_conexion()
    if conexion:
        ejecutar_script(conexion, "db/schema.sql")
