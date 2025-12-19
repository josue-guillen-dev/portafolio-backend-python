from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from passlib.context import CryptContext
import sqlite3

app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def inicializar_db():
    conexion = sqlite3.connect("tienda1.db")
    cursor = conexion.cursor()
    cursor.execute(
        """ CREATE TABLE IF NOT EXISTS usuarios(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT) """
    )
    cursor.execute(
        """ CREATE TABLE IF NOT EXISTS productos(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        stock INTEGER) """
    )
    cursor.execute(
        """ CREATE TABLE IF NOT EXISTS ventas(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        producto_id INTEGER,
        cantidad INTEGER) """
    )
    conexion.commit()
    conexion.close()


inicializar_db()


class Usuarios(BaseModel):
    username: str
    password: str


class Productos(BaseModel):
    nombre: str
    stock: int


class Ventas(BaseModel):
    user_id: int
    producto_id: int
    cantidad: int
    password: str


@app.post("/registro")
def registro(username: Usuarios):
    password_encriptado = pwd_context.hash(username.password)
    conexion = sqlite3.connect("tienda1.db")
    cursor = conexion.cursor()
    cursor.execute(
        "INSERT INTO usuarios (username,password) VALUES (?,?)",
        (username.username, password_encriptado),
    )

    conexion.commit()
    conexion.close()
    return {"mensaje": "usuario registrado"}


@app.post("/registro/admin/productos")
def productos(producto: Productos):
    conexion = sqlite3.connect("tienda1.db")
    cursor = conexion.cursor()
    cursor.execute(
        "INSERT INTO productos (nombre, stock) VALUES (?,?)",
        (producto.nombre, producto.stock),
    )
    conexion.commit()
    conexion.close()
    return {"mensaje": "Producto Registrado"}


@app.post("/comprar")
def comprar(ventas: Ventas):
    conexion = sqlite3.connect("tienda1.db")
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT username , password FROM usuarios WHERE id = ?", (ventas.user_id,)
    )
    usuario = cursor.fetchone()
    
    if usuario is None:
        conexion.close()
        raise HTTPException(status_code=404, detail="usuario no encontrado")
    password_guardada = usuario[1]

    if not pwd_context.verify(ventas.password, password_guardada):
        conexion.close()
        raise HTTPException(status_code=400, detail="contrasena incorrecta")
    cursor.execute(
        "SELECT nombre, stock FROM productos WHERE id = ?", (ventas.producto_id,)
    )
    producto = cursor.fetchone()
    if producto is None:
        conexion.close()
        raise HTTPException(status_code=404, detail="producto no existe")
    stock = producto[1]
    if stock < ventas.cantidad:
        conexion.close()
        raise HTTPException(status_code=400, detail="No hay suficiente stock")

    cursor.execute(
        "UPDATE productos SET stock = stock - ? WHERE id = ?",
        (ventas.cantidad, ventas.producto_id),
    )

    cursor.execute(
        "INSERT INTO ventas (user_id,producto_id,cantidad) VALUES (?,?,?)",
        (ventas.user_id, ventas.producto_id, ventas.cantidad),
    )
    venta_factura = {
        "mensaje": "Venta realizada",
        "Factura": {
            "usuario": usuario[0],
            "producto": producto,
            "cantidad": ventas.cantidad,
        },
    }
    conexion.commit()
    conexion.close()
    return venta_factura
