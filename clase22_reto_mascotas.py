from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import sqlite3

app = FastAPI()


def inicializar_db():
    conexion = sqlite3.connect("mascotas.db")
    cursor = conexion.cursor()

    cursor.execute(
        """ CREATE TABLE IF NOT EXISTS mascotas(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        especie TEXT,
        edad INTEGER) """
    )
    conexion.commit()
    conexion.close()


inicializar_db()


class MascotaNueva(BaseModel):
    nombre: str
    especie: str
    edad: int


@app.post("/mascotas_nueva")
def mascota_nueva(mascota: MascotaNueva):
    conexion = sqlite3.connect("mascotas.db")
    cursor = conexion.cursor()
    cursor.execute(
        "INSERT INTO mascotas (nombre,especie,edad) VALUES (?,?,?)",
        (mascota.nombre, mascota.especie, mascota.edad),
    )
    conexion.commit()
    conexion.close()
    return {"mensaje": "Mascota registrada"}


@app.get("/ver_mascotas")
def ver_mascotas(especie: str):
    conexion = sqlite3.connect("mascotas.db")
    cursor = conexion.cursor()
    if especie:
        cursor.execute("SELECT * FROM mascotas WHERE especie = ?", (especie,))
    else:
        cursor.execute("SELECT * FROM mascotas")
    resultado = cursor.fetchall()

    mascotas = []
    for lista in resultado:
        mascotas.append({
            "id": lista[0],
            "nombre": lista[1],
            "especie": lista[2],
            "edad": lista[3],
        })
    conexion.close()
    return mascotas


@app.put("/mascotas/{id_mascota}/cumpleanos")
def cumpleanos_edad(id_mascota: int):
    conexion = sqlite3.connect("mascotas.db")
    cursor = conexion.cursor()
    cursor.execute("UPDATE mascotas SET edad = edad + 1 WHERE id = ?", (id_mascota,))
    if cursor.rowcount == 0:
        conexion.close()
        raise HTTPException(status_code=404, detail="La mascota no existe")
    conexion.commit()
    conexion.close()
    return {"mensaje": f"Edad de la mascota {id_mascota} aumentada en 1 año"}


@app.delete("/mascotas/{id_mascota}")
def adoptar_mascota(id_mascota: int):
    conexion = sqlite3.connect("mascotas.db")
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM mascotas WHERE id = ?", (id_mascota,))
    resultado = cursor.fetchone()
    conexion.commit()
    if cursor.rowcount == 0:
        conexion.close()
        raise HTTPException(status_code=404, detail="id invalido Mascota no existe")
    conexion.commit()
    conexion.close()
    return {"mensaje": "Mascota dada en adopcion"}
