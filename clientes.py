import json
import os

archivo_json = "clientes.json"

def cargar_datos():
    """Cargar datos desde el archivo JSON."""
    if os.path.exists(archivo_json) and os.path.getsize(archivo_json) > 0:
        with open(archivo_json, "r") as archivo:
            datos = json.load(archivo)
        return datos
    else:
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

def crear_usuario(datos):
    """Crear un nuevo usuario."""
    nuevo_id = obtener_ultimo_id() + 1
    usuario = {
        "id": nuevo_id,
        "nombre": datos['nombre'],
        "apellido": datos['apellido'],
        "direccion": datos['direccion'],
        "codigoAcceso": datos['codigoAcceso'],
        "telefono": datos['telefono']
    }
    datos = cargar_datos()
    datos.append(usuario)
    guardar_datos(datos)