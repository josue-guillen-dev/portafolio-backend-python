from fastapi import FastAPI
import sqlite3

app = FastAPI()

@app.get("/productos")
def obtener_productos():
    conexion = sqlite3.connect("inventario_maestro.db")
    cursor = conexion.cursor()
    
    cursor.execute("SELECT * FROM productos")
    resultado = cursor.fetchall()
    
    conexion.close()
    
    lista_final = []
    
    for producto in resultado:
        item = {
            "id": producto[0],
            "nombre": producto[1],
            "precio": producto[2],
            "stock": producto[3]
        }
        lista_final.append(item)
    return lista_final