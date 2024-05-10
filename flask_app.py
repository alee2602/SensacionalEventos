from flask import Flask, render_template, request, redirect, url_for,jsonify,flash,session
from flask_bootstrap import Bootstrap
#from clientes import cargar_datos, guardar_datos, obtener_ultimo_id, crear_usuario,obtener_usuario_por_id,editarUsuario,eliminarUsuario
#from pedidos import  crear_pedido, editar_pedido,obtener_pedido_por_id,eliminar_pedido, cambiar_estado_pedido
import json
from db.conexiondb import verificar_credenciales,obtener_inventario,editar_inventario,eliminar_inventario,insertar_producto,obtener_clientes_bd,eliminar_cliente,editar_cliente_bd,crear_cliente_bd,crear_pedido_bd,editar_pedido_bd,eliminar_pedido_bd,obtener_pedido_por_id_bd,cambiar_estado_pedido_bd, obtener_todos_los_pedidos
from pdf import generar_pdf
from functools import wraps
import secrets

app = Flask(__name__)
Bootstrap(app)
app.secret_key=secrets.token_hex(16)




@app.route('/index')
def index():
    return render_template('index.html')

###################################################################
#                           LOGIN                                 #
###################################################################
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(username)
        ver=verificar_credenciales(username,password)
    

        # Verificar las credenciales del usuario en la base de datos
        #usuario = verificar_credenciales(username, password)


        if ver!=None and (username == ver[2] and password == ver[3]):
            print("si")    
            return render_template('index.html')
        else:
            return render_template('AuthError.html')  # Redirigir a la página AuthError.html
        
    return render_template('login.html')

@app.route('/clientes')
def clientes():
    clientes = obtener_clientes_bd()
    print(clientes)
    return render_template('clientes.html', clientes=clientes)
@app.route('/pedidos')
def pedidos():
    # Cargar datos de la base de datos 
    pedidos = obtener_todos_los_pedidos()
        
    return render_template('pedidos.html', pedidos=pedidos)

@app.route('/inventario')
def inventario():
    productos = obtener_inventario()
    print("-----------------")
    print(productos)
    print("-----------------")
    return render_template('inventario.html', productos=productos)


@app.route('/crear_cliente', methods=['GET', 'POST'])
def crear_cliente_route():
    if request.method == 'POST':
        datos_usuario = {
            'nombre': request.form['nombre'],
            'apellido': request.form['apellido'],
            'direccion': request.form['direccion'],
            'codigoAcceso': request.form['codigoAcceso'],
            'telefono': request.form['telefono']
        }
        datos_usuario=[request.form['nombre'],request.form['apellido'],request.form['direccion'],request.form['codigoAcceso'],request.form['telefono']]
        crear_cliente_bd(datos_usuario)
        return redirect(url_for('clientes'))

    return render_template('crearUsuario.html')

@app.route('/pedidos/cambiar_estado/<int:pedido_id>', methods=['POST'])
def cambiar_estado_pedido_route(pedido_id):
    if request.method == 'POST':
        cambiar_estado_pedido_bd(pedido_id)
        return redirect(url_for('listar_pedidos'))
    else:
        return 'Método no permitido', 405
@app.route('/editar_cliente/<int:cliente_id>', methods=['GET', 'POST'])
def editar_cliente(cliente_id):
    if request.method == 'POST':
        nuevos_datos = {
            'nombre': request.form['nombre'],
            'apellido': request.form['apellido'],
            'direccion': request.form['direccion'],
            'codigoAcceso': request.form['codigoAcceso'],
            'telefono': request.form['telefono']
        }
        nuevos_datos=[request.form['nombre'],request.form['apellido'],request.form['direccion'],request.form['codigoAcceso'],request.form['telefono']]
        editar_cliente_bd(cliente_id, nuevos_datos)  # Aquí pasamos cliente_id como el primer argumento
        return redirect(url_for('clientes'))

    return render_template('clientes.html', clientes=obtener_clientes_bd())




@app.route('/eliminar_usuario/<int:usuario_id>')
def eliminar_usuario(usuario_id):
    eliminar_cliente(usuario_id)
    return redirect('/clientes')

# Rutas para la página de pedidos
@app.route('/pedidos')
def listar_pedidos():
    pedidos = obtener_todos_los_pedidos()
    return render_template('pedidos.html', pedidos=pedidos)


def obtener_cantidad_pedido_producto(pedido, producto_id):
    """Obtener la cantidad de un producto en un pedido."""
    for detalle in pedido.get("detalles", []):
        if detalle["producto_id"] == producto_id:
            return detalle["cantidad"]
    return 0

@app.route('/pedidos/nuevo', methods=['GET', 'POST'])
def crear_pedido_route():
    clientes = obtener_clientes_bd()
    productos = obtener_inventario()

    if request.method == 'POST':
        #nuevo_pedido=[str(request.form.get('idCliente')),request.form.get('comentarios'),request.form.get('descripcion'),request.form.get('fechaEntrega'),'Pendiente',request.form.get('fechaRecoger'),'pendiente',request.form.get('total')]
        nuevo_pedido=[str(request.form.get('idCliente')),request.form.get('comentarios'),str(request.form.get('descripcion')).replace(":","---")+", ",request.form.get('fechaEntrega'),request.form.get('fechaRecoger'),'pendiente',request.form.get('total')]
        print(nuevo_pedido)
        
        if crear_pedido_bd(nuevo_pedido):
            print("sisisiis")
        else:
            print("nononono")
        generar_pdf(nuevo_pedido[0],nuevo_pedido[2],nuevo_pedido[6],nuevo_pedido[3],nuevo_pedido[4])

    return render_template('formulario_pedido.html', clientes=clientes, productos=productos)

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
    clientes = obtener_clientes_bd()
    pedido = obtener_pedido_por_id_bd(pedido_id)
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
        editar_pedido_bd(pedido_id, nuevos_datos)
        return redirect(url_for('listar_pedidos'))
    else:
        return render_template('formulario_pedido.html', pedido=pedido, clientes=clientes)

@app.route('/pedidos/eliminar/<int:pedido_id>')
def eliminar_pedido_route(pedido_id):
    if eliminar_pedido_bd(pedido_id):
        return redirect(url_for('listar_pedidos'))
    else:
        return 'Pedido no encontrado', 404
@app.route('/crear_producto', methods=['GET', 'POST'])
def crear_producto_route():
    if request.method == 'POST':
        datos_producto = (
            request.form['producto'],
            request.form['marca'],
            float(request.form['valor']),
            float(request.form['precio']),
            request.form['cantidad'],
            request.form['comentarios']
        )
        insertar_producto(datos_producto)
        return redirect(url_for('inventario'))

    return render_template('crear_producto.html')


@app.route('/editar_producto/<int:producto_id>', methods=['GET', 'POST'])
def editar_producto_route(producto_id):

    if request.method == 'POST':
        nuevos_datos=[request.form['producto'],request.form['marca'],request.form['valor'],request.form['precio'],request.form['cantidad'],request.form['comentarios']]
        print(nuevos_datos)
        editar_inventario(producto_id, nuevos_datos)
        return redirect(url_for('inventario'))

    

@app.route('/eliminar_producto/<int:producto_id>')
def eliminar_producto_route(producto_id):
    eliminar_inventario(producto_id)
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

if __name__ == 'main':
    app.run(debug=True)
