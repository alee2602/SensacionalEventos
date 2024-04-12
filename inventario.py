import json
import os

archivo_json = "inventario.json"

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

def obtener_ultimo_id(datos):
    """Obtener el último ID utilizado."""
    if datos:
        return max(item["id"] for item in datos)
    else:
        return 0

def editar_producto(producto_id, nuevos_datos):
    """Editar los datos de un producto por su ID."""
    datos = cargar_datos()
    for item in datos:
        if item["id"] == producto_id:
            item.update(nuevos_datos)
            guardar_datos(datos)
            return True
    return False

def obtener_producto_por_id(producto_id):
    """Obtener un producto por su ID."""
    datos = cargar_datos()
    for item in datos:
        if item["id"] == producto_id:
            return item
    return None

def eliminar_producto(producto_id):
    """Eliminar un producto por su ID."""
    datos = cargar_datos()
    for i, item in enumerate(datos):
        if item["id"] == producto_id:
            del datos[i]
            guardar_datos(datos)
            return True
    return False

def crear_producto(datos):
    """Crear un nuevo producto."""
    nuevo_id = obtener_ultimo_id(cargar_datos()) + 1
    producto = {
        "id": nuevo_id,
        "producto": datos['producto'],
        "marca": datos['marca'],
        "valor": float(datos['valor']),
        "precio": float(datos['precio']),
        "cantidad": int(datos['cantidad']),
        "comentarios": datos['comentarios']
    }
    datos = cargar_datos()
    datos.append(producto)
    guardar_datos(datos)
