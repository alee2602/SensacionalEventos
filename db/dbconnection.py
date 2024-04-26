from sqlalchemy import create_engine, Column, Integer, String, Text, DATE, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine('postgresql://postgres:16022004@localhost:5432/sensacionaleventosdb')


Base = declarative_base()

class Cliente(Base):
    __tablename__ = 'cliente'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), nullable=False)
    apellido = Column(String(50), nullable=False)
    direccion = Column(String(50), nullable=False)
    codigo_acceso = Column(String(50), nullable=False)
    telefono = Column(String(50), nullable=False)
    
    pedidos = relationship("Pedidos", back_populates="cliente")

class Inventario(Base):
    __tablename__ = 'inventario'
    
    id = Column(Integer, primary_key=True)
    producto = Column(String(50), nullable=False)
    marca = Column(String(50), nullable=False)
    valor = Column(Integer, nullable=False)
    precio = Column(Float, nullable=False)
    cantidad = Column(Integer, nullable=False)
    comentarios = Column(Text, nullable=False)
    
class Pedidos(Base):
    __tablename__ = 'pedidos'
    id_pedido = Column(Integer, primary_key=True)
    id_cliente = Column(Integer,  ForeignKey('cliente.id'), nullable=False)
    comentarios = Column(Text, nullable=False)
    descripcion_pedido = Column(Text, nullable=False)
    fecha_entrega = Column(DATE, nullable=False)
    fecha_recoger = Column(DATE, nullable=False)
    estado = Column(String(50), nullable=False)
    total = Column(Float, nullable=False)
    
    cliente = relationship("Cliente", back_populates="pedidos")

Session = sessionmaker(engine)
session = Session()

if __name__ == '__main__':

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
