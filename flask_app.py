from flask import Flask, render_template, request, redirect, url_for,jsonify,flash
from flask_bootstrap import Bootstrap
from clientes import cargar_datos, guardar_datos, obtener_ultimo_id, crear_usuario,obtener_usuario_por_id,editarUsuario,eliminarUsuario
from inventario import cargar_datos as cargar_datos_inventario, guardar_datos as guardar_datos_inventario
from inventario import obtener_ultimo_id as obtener_ultimo_id_inventario, crear_producto, obtener_producto_por_id, editar_producto, eliminar_producto
from pedidos import  obtener_productos,obtener_clientes,cargar_datos_pedidos, editar_pedido,obtener_pedido_por_id,eliminar_pedido,guardar_datos_pedidos, obtener_ultimo_id_pedidos, crear_pedido, cambiar_estado_pedido
import json
from db.conexiondb import verificar_credenciales
from pdf import generar_pdf
app = Flask(_name_)
Bootstrap(app)

@app.route('/index')
def index():
    return render_template('index.html')
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(username)
        print(password)

        # Verificar las credenciales del usuario en la base de datos
        #usuario = verificar_credenciales(username, password)

        if (username=="admin" and password=="admin"):
            print("si")    
            return render_template('index.html')  # Redirigir a la página index.html
        else:
            # Si las credenciales son incorrectas, mostrar un mensaje de error
            flash('Credenciales incorrectas. Por favor, inténtalo de nuevo.', 'error')

    return render_template('login.html')
@app.route('/usuarios')
def usuarios():
    usuarios = cargar_datos()
    return render_template('usuarios.html', usuarios=usuarios)
@app.route('/pedidos')
def pedidos():
    # Cargar datos de pedidos.json
    with open('pedidos.json', 'r') as file:
        pedidos = json.load(file)
        

    return render_template('pedidos.html', pedidos=pedidos)

@app.route('/inventario')
def inventario():
    productos = cargar_datos_inventario()
    return render_template('inventario.html', productos=productos)


@app.route('/crear_usuario', methods=['GET', 'POST'])
def crear_usuario_route():
    if request.method == 'POST':
        datos_usuario = {
            'nombre': request.form['nombre'],
            'apellido': request.form['apellido'],
            'direccion': request.form['direccion'],
            'codigoAcceso': request.form['codigoAcceso'],
            'telefono': request.form['telefono']
        }
        crear_usuario(datos_usuario)
        return redirect(url_for('usuarios'))

    return render_template('crearUsuario.html')

@app.route('/pedidos/cambiar_estado/<int:pedido_id>', methods=['POST'])
def cambiar_estado_pedido_route(pedido_id):
    if request.method == 'POST':
        cambiar_estado_pedido(pedido_id)
        return redirect(url_for('listar_pedidos'))
    else:
        return 'Método no permitido', 405

@app.route('/editar_usuario/<int:usuario_id>', methods=['GET', 'POST'])
def editar_usuario(usuario_id):
    usuario = obtener_usuario_por_id(usuario_id)

    if request.method == 'POST':
        nuevos_datos = {
            'nombre': request.form['nombre'],
            'apellido': request.form['apellido'],
            'direccion': request.form['direccion'],
            'codigoAcceso': request.form['codigoAcceso'],
            'telefono': request.form['telefono']
        }
        editarUsuario(usuario_id, nuevos_datos)
        return redirect(url_for('usuarios'))

    return render_template('editar_usuario.html', usuario=usuario)

@app.route('/eliminar_usuario/<int:usuario_id>')
def eliminar_usuario(usuario_id):
    eliminarUsuario(usuario_id)
    return redirect(url_for('usuarios'))

# Rutas para la página de pedidos
@app.route('/pedidos')
def listar_pedidos():
    pedidos = cargar_datos_pedidos()
    return render_template('pedidos.html', pedidos=pedidos)


def obtener_cantidad_pedido_producto(pedido, producto_id):
    """Obtener la cantidad de un producto en un pedido."""
    for detalle in pedido.get("detalles", []):
        if detalle["producto_id"] == producto_id:
            return detalle["cantidad"]
    return 0

@app.route('/pedidos/nuevo', methods=['GET', 'POST'])
def crear_pedido_route():
    clientes = obtener_clientes()
    productos = obtener_productos()

    if request.method == 'POST':
        nuevo_pedido = {
            "idCliente": int(request.form.get('idCliente')),
            "descripcionPedido": request.form.get('descripcion'),
            "comentarios":request.form.get('comentarios'),
            "fechaEntrega": request.form.get('fechaEntrega'),
            "fechaRecoger": request.form.get('fechaRecoger'),
            "estado": "pendiente",
            "total": float(request.form.get('total'))
        }
        print(nuevo_pedido['comentarios'])
        crear_pedido(nuevo_pedido)
        generar_pdf(nuevo_pedido['idCliente'],nuevo_pedido['descripcionPedido'],nuevo_pedido['total'],nuevo_pedido['fechaEntrega'],nuevo_pedido['fechaRecoger'])

    return render_template('formulario_pedido.html', clientes=clientes, productos=productos)

def actualizar_inventario_pedido(formulario, productos):
    """Actualizar el inventario al procesar un nuevo pedido."""
    try:
        for producto in productos:
            cantidad_pedido = int(formulario.get(f'cantidad_{producto["id"]}', 0))
            if cantidad_pedido > 0:
                cantidad_disponible = producto["cantidad"]
                if cantidad_pedido > cantidad_disponible:
                    # Si no hay suficiente cantidad disponible, abortar la actualización
                    return False
                else:
                    # Restar la cantidad pedida del inventario
                    producto["cantidad"] -= cantidad_pedido

        # Guardar los cambios en el archivo de inventario
        guardar_datos_inventario(productos)
        return True

    except Exception as e:
        # Manejar cualquier excepción que pueda ocurrir durante la actualización del inventario
        print(f"Error al actualizar el inventario: {str(e)}")
        return False
def generar_descripcion_pedido(formulario, productos):
    """Generar la descripción del pedido a partir del formulario."""
    detalles = []
    for producto in productos:
        cantidad = int(formulario.get(f'cantidad_{producto["id"]}', 0))
        if cantidad > 0:
            detalles.append({
                "producto_id": producto["id"],
                "producto_nombre": producto["nombre"],
                "cantidad": cantidad,
                "precio_unitario": producto["precio"]
            })

    return json.dumps(detalles)

def calcular_total_pedido(formulario, productos):
    """Calcular el total del pedido a partir del formulario."""
    total = 0
    for producto in productos:
        cantidad = int(formulario.get(f'cantidad_{producto["id"]}', 0))
        total += cantidad * producto["precio"]

    return total
@app.route('/pedidos/editar/<int:pedido_id>', methods=['GET', 'POST'])
def editar_pedido_route(pedido_id):
    clientes = obtener_clientes()
    pedido = obtener_pedido_por_id(pedido_id)
    if not pedido:
        return 'Pedido no encontrado', 404

    if request.method == 'POST':
        nuevos_datos = {
            "idCliente": int(request.form.get('idCliente')),
            "descripcionPedido": request.form.get('descripcion'),
            "comentarios":request.form.get('comentarios'),
            "fechaEntrega": request.form.get('fechaEntrega'),
            "fechaRecoger": request.form.get('fechaRecoger'),
            "estado": "pendiente",
            "total": float(request.form.get('total'))
        }
        editar_pedido(pedido_id, nuevos_datos)
        return redirect(url_for('listar_pedidos'))
    else:
        return render_template('formulario_pedido.html', pedido=pedido, clientes=clientes)

@app.route('/pedidos/eliminar/<int:pedido_id>')
def eliminar_pedido_route(pedido_id):
    if eliminar_pedido(pedido_id):
        return redirect(url_for('listar_pedidos'))
    else:
        return 'Pedido no encontrado', 404
@app.route('/crear_producto', methods=['GET', 'POST'])
def crear_producto_route():
    if request.method == 'POST':
        datos_producto = {
            'producto': request.form['producto'],
            'marca': request.form['marca'],
            'valor': float(request.form['valor']),
            'precio': float(request.form['precio']),
            'cantidad': request.form['cantidad'],
            'comentarios': request.form['comentarios']
        }
        crear_producto(datos_producto)
        return redirect(url_for('inventario'))

    return render_template('crear_producto.html')

@app.route('/editar_producto/<int:producto_id>', methods=['GET', 'POST'])
def editar_producto_route(producto_id):
    producto = obtener_producto_por_id(producto_id)

    if request.method == 'POST':
        nuevos_datos = {
            'producto': request.form['producto'],
            'marca': request.form['marca'],
            'valor': request.form['valor'],
            'precio': request.form['precio'],
            'cantidad': request.form['cantidad'],
            'comentarios': request.form['comentarios']
        }
        editar_producto(producto_id, nuevos_datos)
        return redirect(url_for('inventario'))

    return render_template('editar_producto.html', producto=producto)

@app.route('/eliminar_producto/<int:producto_id>')
def eliminar_producto_route(producto_id):
    eliminar_producto(producto_id)
    return redirect(url_for('inventario'))
@app.route('/actualizar_inventario/<int:producto_id>/<int:cantidad>', methods=['POST'])
def actualizar_inventario(producto_id, cantidad):
    # Lógica para actualizar el inventario
    inventario_file = "inventario.json"

    try:
        with open(inventario_file, 'r') as file:
            inventario = json.load(file)

        # Buscar el producto en el inventario
        for producto in inventario:
            if producto['id'] == producto_id:
                if producto['cantidad'] >= cantidad:
                    producto['cantidad'] -= cantidad
                    # Guardar los cambios en el archivo
                    with open(inventario_file, 'w') as file:
                        json.dump(inventario, file, indent=2)
                    return jsonify({'success': True, 'message': 'Inventario actualizado correctamente'})
                else:
                    return jsonify({'success': False, 'message': 'No hay suficiente cantidad en el inventario'})
        
        return jsonify({'success': False, 'message': 'Producto no encontrado en el inventario'})

    except FileNotFoundError:
        return jsonify({'success': False, 'message': 'El archivo de inventario no existe'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})



# Resto del código...

if _name_ == '_main_':
    app.run(debug=True)