import json
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.dbconnection import Cliente


engine = create_engine('postgresql://postgres:16022004@localhost:5432/sensacionaleventosdb')


Session = sessionmaker(bind=engine)
session = Session()

archivo_json = "clientes.json"

def cargar_datos():
    try:
        clientes = session.query(Cliente).all()
        return clientes
    except Exception as e:
        print("Error al obtener los clientes:", e)
        return []

def guardar_datos(datos):
    """Guardar datos en el archivo JSON."""
    with open(archivo_json, "w") as archivo:
        json.dump(datos, archivo, indent=2)

def obtener_ultimo_id():
    """Obtener el último ID utilizado."""
    datos = cargar_datos()
    if datos:
        return max(usuario["id"] for usuario in datos)
    else:
        return 0
    
def editarUsuario(usuario_id, nuevos_datos):
    try:
        cliente = session.query(Cliente).filter_by(id=usuario_id).first()
        if cliente:
            for key, value in nuevos_datos.items():
                setattr(cliente, key, value)
            session.commit()
            print(f"Cliente con ID {usuario_id} editado correctamente.")
            return True
        else:
            print(f"No se encontró un cliente con ID {usuario_id}.")
            return False
    except Exception as e:
        session.rollback()  
        print("Error al editar el cliente:", e)
        return False

def obtener_usuario_por_id(usuario_id):
    try:
        cliente = session.query(Cliente).filter_by(id=usuario_id).first()
        if cliente:
            return cliente  
        else:
            print(f"No se encontró un cliente con ID {usuario_id}.")
            return None
    except Exception as e:
        print("Error al obtener el cliente por ID:", e)
        return None
    
def eliminarUsuario(usuario_id):
    try:
        cliente = session.query(Cliente).filter_by(id=usuario_id).first()
        if cliente:
            session.delete(cliente)
            session.commit()
            print(f"Cliente con ID {usuario_id} eliminado correctamente.")
            return True
        else:
            print(f"No se encontró un cliente con ID {usuario_id}.")
            return False
    except Exception as e:
        session.rollback()  
        print("Error al eliminar el cliente:", e)
        return False

def crear_usuario(datos_cliente):
    try:
        nuevo_cliente = Cliente(**datos_cliente)
        session.add(nuevo_cliente)
        session.commit()
        print("Cliente creado exitosamente.")
        return nuevo_cliente
    except Exception as e:
        session.rollback()  
        print("Error al crear el cliente:", e)
        return None