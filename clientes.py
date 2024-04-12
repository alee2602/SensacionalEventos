import json
import os

archivo_json = "usuarios.json"

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