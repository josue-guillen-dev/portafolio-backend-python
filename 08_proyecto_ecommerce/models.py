from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


# Tabla de Usuarios
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    email = Column(String, unique=True, index=True)  # Email único
    password = Column(String)  # Aquí va el Hash
    es_admin = Column(Boolean, default=False)  # Para saber si es jefe

    # Aquí dejaremos espacio para relacionarlo con sus pedidos en el futuro...
    # pedidos = relationship("Pedido", back_populates="cliente")


# ... (codigo anterior de Usuario) ...


# Tabla de Productos
class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    precio = Column(Integer)
    stock = Column(Integer)
    # descripcion = Column(String) # Opcional si quieres


# models.py


# Tabla de Pedidos (La Cabecera)
class Pedido(Base):
    __tablename__ = "pedidos"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    total = Column(Integer)


# Tabla Intermedia (El Detalle: Qué productos van en qué pedido)
class DetallePedido(Base):
    __tablename__ = "detalle_pedidos"
    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"))
    producto_id = Column(Integer, ForeignKey("productos.id"))
    cantidad = Column(Integer)
    precio_unitario = Column(Integer)  # Precio al momento de la compra


#### 2. Edita `schemas.py` (Cómo recibimos el pedido)

""" El usuario no va a mandar "ID de pedido". Va a mandar una lista de productos y cantidades.

Copia esto al final de `schemas.py`: """
