import json
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.dbconnection import Pedidos


engine = create_engine('postgresql://postgres:16022004@localhost:5432/sensacionaleventosdb')


Session = sessionmaker(bind=engine)
session = Session()

archivo_pedidos = "pedidos.json"

def cargar_datos_pedidos():
    try:
        pedidos = session.query(Pedidos).all()
        return pedidos
    except Exception as e:
        print("Error al obtener el inventario:", e)
        return []

def guardar_datos_pedidos(datos):
    """Guardar datos en el archivo JSON de pedidos."""
    with open(archivo_pedidos, "w") as archivo:
        json.dump(datos, archivo, indent=2)

def obtener_ultimo_id_pedidos():
    """Obtener el último ID de pedido utilizado."""
    datos = cargar_datos_pedidos()
    if datos:
        return max(pedido["idPedido"] for pedido in datos)
    else:
        return 0

def crear_pedido(datos_pedido):
    try:
        nuevo_pedido = Pedidos(**datos_pedido)
        session.add(nuevo_pedido)
        session.commit()
        print("Pedido creado exitosamente.")
        return nuevo_pedido
    except Exception as e:
        session.rollback()  
        print("Error al crear el pedido:", e)
        return None

def editar_pedido(id_pedido, nuevos_datos):
    try:
        pedido = session.query(Pedidos).filter_by(id=id_pedido).first()
        if pedido:
            for key, value in nuevos_datos.items():
                setattr(pedido, key, value)
            session.commit()
            print(f"Pedido con ID {id_pedido} editado correctamente.")
            return True
        else:
            print(f"No se encontró un pedido con ID {id_pedido}.")
            return False
    except Exception as e:
        session.rollback()  
        print("Error al editar el pedido:", e)
        return False

def obtener_pedido_por_id(id_pedido):
    try:
        pedido = session.query(Pedidos).filter_by(id=id_pedido).first()
        if pedido:
            return pedido 
        else:
            print(f"No se encontró un pedido con ID {id_pedido}.")
            return None
    except Exception as e:
        print("Error al obtener el pedido por ID:", e)
        return None

def eliminar_pedido(id_pedido):
    try:
        pedido = session.query(Pedidos).filter_by(id=id_pedido).first()
        if pedido:
            session.delete(pedido)
            session.commit()
            print(f"Pedido con ID {id_pedido} eliminado correctamente.")
            return True
        else:
            print(f"No se encontró un pedido con ID {id_pedido}.")
            return False
    except Exception as e:
        session.rollback()  
        print("Error al eliminar el pedido:", e)
        return False

def obtener_clientes():
    """Obtener la lista de clientes."""
    with open("clientes.json", "r") as archivo_clientes:
        clientes = json.load(archivo_clientes)
    return clientes
def obtener_productos():
    with open("inventario.json", "r") as archivo_productos:
        productos = json.load(archivo_productos)
    return productos

def cambiar_estado_pedido(pedido_id):
    pedidos = cargar_datos_pedidos()

    for pedido in pedidos:
        if pedido['idPedido'] == pedido_id:
            if pedido['estado'] == 'pendiente':
                pedido['estado'] = 'finalizado'
            elif pedido['estado'] == 'finalizado':
                pedido['estado'] = 'pendiente'
            break

    guardar_datos_pedidos(pedidos)

def guardar_datos_pedidos(pedidos):
    with open('pedidos.json', 'w') as file:
        json.dump(pedidos, file, indent=2)
