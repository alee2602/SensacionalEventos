import json
import os

archivo_pedidos = "pedidos.json"

def cargar_datos_pedidos():
    """Cargar datos desde el archivo JSON de pedidos."""
    if os.path.exists(archivo_pedidos) and os.path.getsize(archivo_pedidos) > 0:
        with open(archivo_pedidos, "r") as archivo:
            datos = json.load(archivo)
        return datos
    else:
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
    """Crear un nuevo pedido."""
    nuevo_id = obtener_ultimo_id_pedidos() + 1
    pedido = {
        "idPedido": nuevo_id,
        "idCliente": datos_pedido["idCliente"],
        "comentarios": datos_pedido["comentarios"],
        "descripcionPedido": datos_pedido["descripcionPedido"],
        "fechaEntrega": datos_pedido["fechaEntrega"],
        "fechaRecoger": datos_pedido["fechaRecoger"],
        "estado": datos_pedido["estado"],
        "total": datos_pedido["total"]
    }
    datos = cargar_datos_pedidos()
    datos.append(pedido)
    guardar_datos_pedidos(datos)

def editar_pedido(id_pedido, nuevos_datos):
    """Editar los datos de un pedido por su ID."""
    datos = cargar_datos_pedidos()
    for pedido in datos:
        if pedido["idPedido"] == id_pedido:
            pedido.update(nuevos_datos)
            guardar_datos_pedidos(datos)
            return True
    return False

def obtener_pedido_por_id(id_pedido):
    """Obtener un pedido por su ID."""
    datos = cargar_datos_pedidos()
    for pedido in datos:
        if pedido["idPedido"] == id_pedido:
            return pedido
    return None

def eliminar_pedido(id_pedido):
    """Eliminar un pedido por su ID."""
    datos = cargar_datos_pedidos()
    for i, pedido in enumerate(datos):
        if pedido["idPedido"] == id_pedido:
            del datos[i]
            guardar_datos_pedidos(datos)
            return True
    return False
def obtener_clientes():
    """Obtener la lista de clientes."""
    with open("usuarios.json", "r") as archivo_clientes:
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
