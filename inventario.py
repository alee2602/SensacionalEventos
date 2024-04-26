import json
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.dbconnection import Inventario


engine = create_engine('postgresql://postgres:16022004@localhost:5432/sensacionaleventosdb')


Session = sessionmaker(bind=engine)
session = Session()

archivo_json = "inventario.json"

def cargar_datos():
    try:
        inventario = session.query(Inventario).all()
        return inventario
    except Exception as e:
        print("Error al obtener el inventario:", e)
        return []

def guardar_datos(datos):
    """Guardar datos en el archivo JSON."""
    with open(archivo_json, "w") as archivo:
        json.dump(datos, archivo, indent=2)

def obtener_ultimo_id(datos):
    """Obtener el último ID utilizado."""
    if datos:
        return max(item["id"] for item in datos)
    else:
        return 0

def editar_producto(producto_id, nuevos_datos):
    try:
        producto = session.query(Inventario).filter_by(id=producto_id).first()
        if producto:
            for key, value in nuevos_datos.items():
                setattr(producto, key, value)
            session.commit()
            print(f"Producto con ID {producto_id} editado correctamente.")
            return True
        else:
            print(f"No se encontró un producto con ID {producto_id}.")
            return False
    except Exception as e:
        session.rollback()  
        print("Error al editar el producto:", e)
        return False

def obtener_producto_por_id(producto_id):
    try:
        producto = session.query(Inventario).filter_by(id=producto_id).first()
        if producto:
            return producto  
        else:
            print(f"No se encontró un producto con ID {producto_id}.")
            return None
    except Exception as e:
        print("Error al obtener el producto por ID:", e)
        return None

def eliminar_producto(producto_id):
    try:
        producto = session.query(Inventario).filter_by(id=producto_id).first()
        if producto:
            session.delete(producto)
            session.commit()
            print(f"Producto con ID {producto_id} eliminado correctamente.")
            return True
        else:
            print(f"No se encontró un producto con ID {producto_id}.")
            return False
    except Exception as e:
        session.rollback()  
        print("Error al eliminar el producto:", e)
        return False

def crear_producto(datos_producto):
    try:
        nuevo_producto = Inventario(**datos_producto)
        session.add(nuevo_producto)
        session.commit()
        print("Cliente creado exitosamente.")
        return nuevo_producto
    except Exception as e:
        session.rollback()  
        print("Error al crear el cliente:", e)
        return None
