from flask import Flask, render_template, request, redirect, url_for,jsonify,flash
from flask_bootstrap import Bootstrap
from clientes import cargar_datos, guardar_datos, obtener_ultimo_id, crear_usuario,obtener_usuario_por_id,editarUsuario,eliminarUsuario
from inventario import cargar_datos as cargar_datos_inventario, guardar_datos as guardar_datos_inventario
from inventario import obtener_ultimo_id as obtener_ultimo_id_inventario, crear_producto, obtener_producto_por_id, editar_producto, eliminar_producto
from pedidos import  obtener_productos,obtener_clientes,cargar_datos_pedidos, editar_pedido,obtener_pedido_por_id,eliminar_pedido,guardar_datos_pedidos, obtener_ultimo_id_pedidos, crear_pedido, cambiar_estado_pedido
import json
from pdf import generar_pdf
app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def index():
    return render_template('index.html')

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
