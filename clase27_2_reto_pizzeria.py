from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import sqlite3

app = FastAPI()


def inicializar_db():
    conexion = sqlite3.connect("pizzeria.db")
    cursor = conexion.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    cursor.execute(
        """ CREATE TABLE IF NOT EXISTS clientes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        direccion TEXT) """
    )
    cursor.execute(
        """ CREATE TABLE IF NOT EXISTS pedidos(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        descripcion TEXT,
        total INTEGER,
        cliente_id INTEGER,
        FOREIGN KEY (cliente_id) REFERENCES clientes(id)) """
    )
    conexion.commit()
    conexion.close()


inicializar_db()


class ClienteNuevo(BaseModel):
    nombre: str
    direccion: str


class PedidoNuevo(BaseModel):
    descripcion: str
    total: int


@app.post("/clientes")
def crear_cleinte(cliente: ClienteNuevo):
    conexion = sqlite3.connect("pizzeria.db")
    cursor = conexion.cursor()
    cursor.execute(
        "INSERT INTO clientes (nombre, direccion) VALUES (?,?)",
        (cliente.nombre, cliente.direccion),
    )
    conexion.commit()
    cliente_id = cursor.lastrowid
    conexion.close()

    return {"mensaje": "Cliente guardado", "id": cliente_id}


@app.post("/clientes/{cliente_id}/pedidos")
def recibir_pedido(cliente_id: int, pedido: PedidoNuevo):
    conexion = sqlite3.connect("pizzeria.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM clientes WHERE id = ?", (cliente_id,))
    cliente = cursor.fetchone()
    if cliente is None:
        conexion.close()
        raise HTTPException(status_code=404, detail="Cliente no existe")

    cursor.execute(
        "INSERT INTO pedidos (descripcion,total,cliente_id) VALUES (?,?,?)",
        (pedido.descripcion, pedido.total, cliente_id),
    )

    conexion.commit()
    pedido_id = cursor.lastrowid
    conexion.close()
    return {"mensaje": "Pedido creado", "pedido": pedido_id, "cliente": cliente_id}


@app.get("/cliente/{cliente_id}/historial")
def buscar_cliente(cliente_id: int):
    conexion = sqlite3.connect("pizzeria.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM clientes WHERE id = ?", (cliente_id,))
    cliente = cursor.fetchone()
    if cliente is None:
        conexion.close()
        raise HTTPException(status_code=404, detail="Cliente no existe")

    cursor.execute("SELECT * FROM pedidos WHERE cliente_id = ?", (cliente_id,))
    pedidos = cursor.fetchall()
    conexion.close()
    historial_pedido = []
    total_gastado = 0
    for pedido in pedidos:
        historial_pedido.append({"descripcion": pedido[1], "gasto_total": pedido[2]})

        total_gastado += pedido[2]

    pedidos_historial = {
        "cliente": cliente[1],
        "direccion": cliente[2],
        "total_gastado": total_gastado,
        "pedidos": historial_pedido,
    }
    return pedidos_historial
