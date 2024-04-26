import json
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.dbconnection import Cliente


engine = create_engine('postgresql://postgres:16022004@localhost:5432/pythondb')


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
    """Editar los datos de un usuario por su ID."""
    datos = cargar_datos()
    for usuario in datos:
        if usuario["id"] == usuario_id:
            usuario.update(nuevos_datos)
            guardar_datos(datos)
            return True
    return False

def obtener_usuario_por_id(usuario_id):
    """Obtener un usuario por su ID."""
    datos = cargar_datos()
    for usuario in datos:
        if usuario["id"] == usuario_id:
            return usuario
    return None
def eliminarUsuario(usuario_id):
    """Eliminar un usuario por su ID."""
    datos = cargar_datos()
    for i, usuario in enumerate(datos):
        if usuario["id"] == usuario_id:
            del datos[i]
            guardar_datos(datos)
            return True
    return False

def crear_usuario(datos_cliente):
    try:
        nuevo_cliente = Cliente(**datos_cliente)
        session.add(nuevo_cliente)
        session.commit()
        print("Cliente creado exitosamente.")
        return nuevo_cliente
    except Exception as e:
        session.rollback()  # Revierte los cambios en caso de error
        print("Error al crear el cliente:", e)
        return None