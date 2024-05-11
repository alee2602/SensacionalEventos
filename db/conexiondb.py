# conexion.py
import psycopg2
from psycopg2 import Error
import os

script_directorio = os.path.dirname(os.path.abspath(_file_))

os.chdir(script_directorio)

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
    cursor = None
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
        if cursor:
            cursor.close()
        if conexion:
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
    
###################################################################
#                           INVENTARIO                            #
###################################################################
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
###################################################################
#                           CLIENTES                              #
###################################################################
def obtener_clientes_bd_byId(id_cliente):
    try:
        conexion = crear_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM clientes WHERE id=%s", (id_cliente,))
        cliente = cursor.fetchone()
        if cliente:
                # Convertir la tupla en un diccionario
                cliente_dict = {
                    'id': cliente[0],
                    'nombre': cliente[1],
                    'apellido': cliente[2],
                    'direccion': cliente[3],
                    'codigoAcceso': cliente[4],
                    'telefono': cliente[5]
                }
                return cliente_dict
        return None
    except Exception as error:
        print("Error al obtener información del cliente:", error)
        #return None
        
def obtener_clientes_bd():
    try:
        conexion=crear_conexion()
        cursor = conexion.cursor()

        # Consulta para verificar las credenciales del usuario
        query = "SELECT * FROM clientes"
        cursor.execute(query)
        clientes = cursor.fetchall()

        cursor.close()
        conexion.close()

        return clientes

    except (Exception, Error) as error:
        print("Error al verificar las credenciales:", error)
        return None
def eliminar_cliente(id):
    try:
        conexion = crear_conexion()
        cursor = conexion.cursor()

        # Consulta para eliminar un registro del inventario
        query = "DELETE FROM clientes WHERE id=%s"  # Usamos %s como marcador de posición para el valor del id
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
def editar_cliente_bd(id, nuevos_datos):
    try:
        conexion = crear_conexion()
        cursor = conexion.cursor()
        print("88888888")
        print(id)
        print(nuevos_datos)
        print("88888888")

        # Consulta para actualizar los datos del inventario
        query = "UPDATE clientes SET nombre = %s, apellido = %s, direccion = %s, codigoacceso = %s, telefono = %s WHERE id = %s"
        cursor.execute(query, (nuevos_datos[0], nuevos_datos[1], nuevos_datos[2], nuevos_datos[3], nuevos_datos[4], id))

        # Confirmar la transacción
        conexion.commit()

    except Exception as e:
        # Manejar cualquier error que pueda ocurrir durante la edición del inventario
        print(f"Error al editar el cliente: {e}")
        conexion.rollback()

    finally:
        # Cerrar el cursor y la conexión
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()
def crear_cliente_bd(producto):
    try:
        conexion = crear_conexion()
        cursor = conexion.cursor()

        # Consulta para insertar un nuevo producto en el inventario
        query = "INSERT INTO clientes (nombre, apellido, direccion, codigoacceso, telefono) VALUES (%s, %s, %s, %s, %s)"
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

###################################################################
#                           PEDIDOS                               #
###################################################################

def crear_pedido_bd(pedido):
    try:
        conexion = crear_conexion()
        with conexion:
            with conexion.cursor() as cursor:
                query = """
                INSERT INTO pedidos (
                    id_cliente, comentarios, descripcion_pedido, fecha_entrega, fecha_recoger, estado, total
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, pedido)
                conexion.commit() #Confirmar la transacción 
                return True
    except (Exception, Error) as error:
        print("Error al insertar el nuevo pedido:", error)
        #return False
        
def editar_pedido_bd(id_pedido, nuevos_datos):
    try:
        conexion = crear_conexion()
        with conexion:
            with conexion.cursor() as cursor:
                query = """
                UPDATE pedidos SET
                    id_cliente = %s,
                    comentarios = %s,
                    descripcion_pedido = %s,
                    fecha_entrega = %s,
                    fecha_recoger = %s,
                    estado = %s,
                    total = %s
                WHERE id_pedido = %s;
                """
                # Crear una tupla con los datos que se actualizarán
                datos_actualizados = (
                    nuevos_datos["id_cliente"],
                    nuevos_datos["comentarios"],
                    nuevos_datos["descripcion_pedido"],
                    nuevos_datos["fecha_entrega"],
                    nuevos_datos["fecha_recoger"],
                    nuevos_datos["estado"],
                    nuevos_datos["total"],
                    id_pedido  
                )
                cursor.execute(query, datos_actualizados)
                conexion.commit()
                return cursor.rowcount > 0  # Retorna True si se actualizó al menos un registro
    except (Exception, Error) as error:
        print("Error al editar el pedido:", error)
        #return False

def eliminar_pedido_bd(id_pedido):
    try:
        conexion = crear_conexion()
        with conexion:
            with conexion.cursor() as cursor:
                # Consulta SQL para eliminar el pedido específico
                query = "DELETE FROM pedidos WHERE id_pedido = %s;"
                cursor.execute(query, (id_pedido,))
                conexion.commit()
                return cursor.rowcount > 0  # Retorna True si se eliminó al menos un registro
    except (Exception, Error) as error:
        print("Error al eliminar el pedido:", error)
        #return False

def obtener_pedido_por_id_bd(id_pedido):
    try:
        conexion = crear_conexion()
        with conexion:
            with conexion.cursor() as cursor:
                # Consulta SQL para obtener el pedido por ID
                query = "SELECT * FROM pedidos WHERE id_pedido = %s;"
                cursor.execute(query, (id_pedido,))
                pedido = cursor.fetchone()  # Obtener el primer resultado
                if pedido:
                    return {
                        "id_pedido": pedido[0],
                        "id_cliente": pedido[1],
                        "comentarios": pedido[2],
                        "descripcion_pedido": pedido[3],
                        "fecha_entrega": pedido[4],
                        "fecha_recoger": pedido[5],
                        "estado": pedido[6],
                        "total": pedido[7]
                    }
                else:
                    return None  # No se encontró el pedido
    except (Exception, Error) as error:
        print("Error al obtener el pedido por ID:", error)
        #return None

def cambiar_estado_pedido_bd(id_pedido):
    try:
        conexion = crear_conexion()
        with conexion:
            with conexion.cursor() as cursor:
                # Primero, obtener el estado actual del pedido
                cursor.execute("SELECT estado FROM pedidos WHERE id_pedido = %s;", (id_pedido,))
                resultado = cursor.fetchone()
                if resultado is None:
                    print("No se encontró el pedido.")
                    return False

                estado_actual = resultado[0]
                # Definir el nuevo estado basado en el estado actual
                nuevo_estado = 'finalizado' if estado_actual == 'pendiente' else 'pendiente'

                # Ahora, actualizar el estado del pedido
                cursor.execute("UPDATE pedidos SET estado = %s WHERE id_pedido = %s;", (nuevo_estado, id_pedido))
                conexion.commit()
                return cursor.rowcount > 0  # Retorna True si se actualizó al menos un registro
    except (Exception, Error) as error:
        print("Error al cambiar el estado del pedido:", error)
        #return False

def obtener_todos_los_pedidos():
    try:
        conexion = crear_conexion()
        with conexion:
            with conexion.cursor() as cursor:
                cursor.execute("SELECT * FROM pedidos;")
                # Recuperar todos los registros y convertirlos en una lista de diccionarios
                columnas = [desc[0] for desc in cursor.description]
                pedidos = [dict(zip(columnas, row)) for row in cursor.fetchall()]
                return pedidos
    except (Exception, Error) as error:
        print("Error al obtener pedidos:", error)
        #return []

    finally:
        # Cerrar el cursor y la conexión
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()

    return False  # Retornar False en caso de error para indicar que la operación no se completó con éxito

if __name__ == "_main_":
    conexion = crear_conexion()
    if conexion:
        ejecutar_script(conexion, "schema.sql")