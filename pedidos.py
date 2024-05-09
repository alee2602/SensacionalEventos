import json
import os
from db.conexiondb import crear_pedido_bd, editar_pedido_bd, obtener_pedido_por_id_bd, eliminar_pedido_bd, cambiar_estado_pedido_bd

def crear_pedido(datos_pedido):
    """Crear un nuevo pedido."""
    return crear_pedido_bd(datos_pedido)

def editar_pedido(id_pedido, nuevos_datos):
    """Editar los datos de un pedido por su ID."""
    return editar_pedido_bd(id_pedido, nuevos_datos)

def obtener_pedido_por_id(id_pedido):
    """Obtener un pedido por su ID."""
    return obtener_pedido_por_id_bd(id_pedido)

def eliminar_pedido(id_pedido):
    """Eliminar un pedido por su ID."""
    return eliminar_pedido_bd(id_pedido)

def cambiar_estado_pedido(pedido_id):
    """Cambiar el estado de un pedido."""
    return cambiar_estado_pedido_bd(pedido_id)


