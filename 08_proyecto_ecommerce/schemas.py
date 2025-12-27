from pydantic import BaseModel


# 1. Esquema Base (Lo que comparten todos)
class UsuarioBase(BaseModel):
    nombre: str
    email: str


# 2. Esquema para CREAR (Lo que el usuario nos manda)
# Aquí SI pedimos la password
class UsuarioCrear(UsuarioBase):
    password: str


# 3. Esquema para RESPONDER (Lo que devolvemos al frontend)
# Aquí NO incluimos la password, por seguridad.
class UsuarioRespuesta(UsuarioBase):
    id: int
    es_admin: bool

    # Esta configuración le permite a Pydantic leer datos de un objeto ORM
    class Config:
        from_attributes = True  # Antes se llamaba orm_mode = True


# 4. Esquema para LOGIN (Solo email y password)
class UsuarioLogin(BaseModel):
    email: str
    password: str


# ... (codigo anterior de Usuario) ...


# Esquema para CREAR un producto
class ProductoCrear(BaseModel):
    nombre: str
    precio: int
    stock: int


# Esquema para MOSTRAR un producto (con ID)
class ProductoRespuesta(ProductoCrear):
    id: int

    class Config:
        from_attributes = True


# schemas.py


# Un item del carrito
class ItemPedido(BaseModel):
    producto_id: int
    cantidad: int


# El pedido completo (Lista de items)
class PedidoCrear(BaseModel):
    items: list[ItemPedido]  # Una lista de productos


#### 3. Edita `main.py` (La Lógica Maestra)

"""Aquí es donde demuestras tu nivel. Vamos a crear la ruta para comprar.

Lógica que debes implementar:**
1.  Recibe el `PedidoCrear` y el `user_id` (en la URL).
2.  Crea un nuevo `Pedido` (cabecera) y guárdalo para tener un ID.
3.  Recorre la lista de items (`for item in pedido.items`):
    * Busca el producto en la BD para saber su precio real.
    * Crea un `DetallePedido` con el ID del pedido, el producto y el precio.
    * Suma al total.
4.  Actualiza el total del Pedido.
5.  Haz Commit final.

Este es el reto más grande hasta ahora. ¿Te animas a intentar escribir esa ruta `POST /usuarios/{user_id}/pedidos` tú solo (o con ayuda de tus apuntes)? 🛒📦 """
