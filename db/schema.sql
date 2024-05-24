
--Creación de tablas--
CREATE TABLE IF NOT EXISTS Clientes (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    apellido VARCHAR(100),
    direccion VARCHAR(100),
    codigoAcceso VARCHAR(100),
    telefono VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS Inventario (
    id SERIAL PRIMARY KEY,
    producto VARCHAR(100),
    marca VARCHAR(100),
    valor INTEGER,
    precio FLOAT,
    cantidad INTEGER,
    comentarios TEXT
);

CREATE TABLE IF NOT EXISTS Pedidos (
    id_pedido SERIAL PRIMARY KEY,
    id_cliente INTEGER NOT NULL,
    comentarios TEXT,
    descripcion_pedido TEXT,
    fecha_entrega DATE,
    fecha_recoger DATE,
    estado VARCHAR(20),
    total FLOAT,
    FOREIGN KEY (id_cliente) REFERENCES Clientes(id)
);

CREATE TABLE IF NOT EXISTS Roles(
    id serial primary key,
    nombre varchar(200)
);
CREATE TABLE IF NOT EXISTS Usuarios(
    ID_Usuario serial primary key,
    id_Rol integer not null, 
    userName varchar(100),
    password varchar(250),
    FOREIGN KEY (id_Rol) REFERENCES Roles(id)
);

/* Optimización de base de datos*/
CREATE INDEX index_clientes_nombre ON Clientes(nombre);
CREATE INDEX index_clientes_apellido ON Clientes(apellido);
CREATE INDEX index_clientes_codigoAcceso ON Clientes(codigoAcceso);
CREATE INDEX index_inventario_producto ON Inventario(producto);
CREATE INDEX index_inventario_marca ON Inventario(marca);
CREATE INDEX index_inventario_valor ON Inventario(valor);
CREATE INDEX index_inventario_precio ON Inventario(precio);
CREATE INDEX index_inventario_cantidad ON Inventario(cantidad);
CREATE INDEX index_pedidos_id_cliente ON Pedidos(id_cliente);
CREATE INDEX index_pedidos_estado ON Pedidos(estado);
CREATE INDEX index_pedidos_fecha_entrega ON Pedidos(fecha_entrega);
CREATE INDEX index_pedidos_fecha_recoger ON Pedidos(fecha_recoger);
CREATE INDEX index_roles_nombre ON Roles(nombre);
CREATE INDEX index_usuarios_id_rol ON Usuarios(id_Rol);
CREATE INDEX index_usuarios_username ON Usuarios(userName);

