# --- CLASE 18: ENVIAR DATOS (POST) ---
# Este archivo enseña como RECIBIR datos del usuario y guardarlos en SQL.

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI()


# 1. EL MOLDE DE DATOS (Pydantic)
# Esto define qué esperamos recibir del usuario
class ProductoNuevo(BaseModel):
    nombre: str
    precio: int
    stock: int


# 2. LA RUTA POST (Guardar)
# Fíjate que usamos @app.post, no @app.get


@app.get("/productos")
def obtener_productos(precio_max: int= None):
    conexion = sqlite3.connect("inventario_maestro.db")
    cursor = conexion.cursor()
    if precio_max is None:
        cursor.execute("SELECT * FROM productos")
    else:
        cursor.execute("SELECT * FROM productos WHERE precio <= ?",(precio_max,))
        
    resultado = cursor.fetchall()

    conexion.close()

    lista_final = []

    for producto in resultado:
        item = {
            "id": producto[0],
            "nombre": producto[1],
            "precio": producto[2],
            "stock": producto[3],
        }
        lista_final.append(item)
    return lista_final


@app.post("/crear_producto")
def guardar_producto(producto: ProductoNuevo):
    print("Recibiendo datos...", producto)

    # TU MISION: Escribir la logica de SQL aqui adentro
    # ------------------------------------------------
    # 1. Conectar a "inventario_maestro.db"
    conexion = sqlite3.connect("inventario_maestro.db")
    # 2. Crear cursor
    cursor = conexion.cursor()
    # 3. Ejecutar INSERT usando (producto.nombre, producto.precio, producto.stock)
    cursor.execute(
        (producto.nombre, producto.precio, producto.stock),
        "INSERT INTO productos (nombre,precio,stock) VALUES (?,?,?)",
    )
    # 4. Commit y Cerrar
    conexion.commit()
    conexion.close()
    # ------------------------------------------------

    # Retornamos un mensaje de éxito
    return {"mensaje": "Producto guardado correctamente", "datos": producto}


@app.delete("/producto/{id_producto}")
def borrar_producto(id_producto: int):
    conexion = sqlite3.connect("inventario_maestro.db")
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM productos WHERE id = ?", (id_producto,))
    conexion.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="producto no encontrado")
    conexion.close()
    return {"Producto Eliminado"}
    


@app.put("/producto/{id_producto}")
def actualizar_producto(id_producto: int, producto_actualizado: ProductoNuevo):

    conexion = sqlite3.connect("inventario_maestro.db")
    cursor = conexion.cursor()
    cursor.execute(
        "UPDATE productos SET nombre = ?, precio = ?, stock = ? WHERE id = ?",
        (
            producto_actualizado.nombre,
            producto_actualizado.precio,
            producto_actualizado.stock,
            id_producto
        ),
    )
    conexion.commit()
    conexion.close()
    return{"Producto Actualizado"}
    
