from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import sqlite3

app = FastAPI()


def inicializar_db():
    conexion = sqlite3.connect("rentacar.db")
    cursor = conexion.cursor()
    cursor.execute(
        """ CREATE TABLE IF NOT EXISTS autos(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        marca TEXT,
        modelo TEXT,
        precio_diario INTEGER,
        disponible INTEGER) """
    )
    conexion.commit()
    conexion.close()


inicializar_db()


class Auto(BaseModel):
    marca: str
    modelo: str
    precio_diario: int


@app.post("/autos")
def guardar_auto(guardar: Auto):
    conexion = sqlite3.connect("rentacar.db")
    cursor = conexion.cursor()
    cursor.execute(
        "INSERT INTO autos (marca,modelo,precio_diario,disponible) VALUES (?,?,?,1)",
        (guardar.marca, guardar.modelo, guardar.precio_diario),
    )
    conexion.commit()
    conexion.close()
    return {"mensaje": "Auto Guardado"}


@app.get("/autos")
def ver_autos(auto: int = Query(None)):
    conexion = sqlite3.connect("rentacar.db")
    cursor = conexion.cursor()
    if auto == 1:
        cursor.execute("SELECT * FROM autos WHERE disponible = 1")
    else:
        cursor.execute("SELECT * FROM autos")
    resultado = cursor.fetchall()
    ver_autos = []
    for auto in resultado:
        ver_autos.append(
            {
                "id": auto[0],
                "marca": auto[1],
                "modelo": auto[2],
                "precio_diario": auto[3],
                "disponible": auto[4],
            }
        )
    conexion.close()
    return ver_autos


@app.get("/autos/{id_auto}/cotizar")
def cotizar(id_auto: int, dias: int):
    conexion = sqlite3.connect("rentacar.db")
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM autos WHERE id = ?", (id_auto,))
    resultado = cursor.fetchone()
    if resultado is None:
        conexion.close()
        raise HTTPException(status_code=404, detail="ERROR: ID no existe")
    precio_total = resultado[3] * dias
    conexion.close()
    return {"mensaje": f"cotizacion para {dias} dias, total a pagar {precio_total}"}


@app.put("/autos/{id_auto/alquilar")
def alquilar(id_auto: int):
    conexion = sqlite3.connect("rentacar.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM autos WHERE id = ?", (id_auto,))
    resultado = cursor.fetchone()
    if resultado is None:
        conexion.close()
        raise HTTPException(status_code=404, detail="ERROR: ID no existe")

    if resultado[4] == 0:
        conexion.close()
        raise HTTPException(status_code=400, detail="El auto ya esta ocupado")
    else:
        cursor.execute("UPDATE autos SET disponible = 0 WHERE id = ?", (id_auto,))
    conexion.commit()
    conexion.close()
    return {"mensaje": "auto rentado"}


@app.put("/autos/{id_auto/devolver")
def devolver(id_auto: int):
    conexion = sqlite3.connect("rentacar.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM autos WHERE id = ?", (id_auto,))
    resultado = cursor.fetchone()
    if resultado is None:
        conexion.close()
        raise HTTPException(status_code=404, detail="ERROR: ID no existe")
    if resultado[4] == 1:
        conexion.close()
        raise HTTPException(status_code=400 ,detail="El auto ya esta aqui")
    if resultado[4] == 0:
        cursor.execute("UPDATE autos SET disponible = 1 WHERE id = ?", (id_auto,))
    conexion.commit()
    conexion.close()
    return {"mensaje": "auto Devuelto correctamente"}


@app.delete("/autos/{id_auto}")
def vender_auto(id_auto: int):
    conexion = sqlite3.connect("rentacar.db")
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM autos WHERE id = ?", (id_auto,))
    if cursor.rowcount == 0:
        conexion.close()
        raise HTTPException(status_code=404, detail="ID no existe")
    conexion.commit()
    conexion.close()
    return {"mensaje": "Auto vendido correctamente"}
