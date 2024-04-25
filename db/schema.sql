
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



