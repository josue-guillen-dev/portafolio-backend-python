from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import sqlite3

app = FastAPI()


def inicializar_db():
    conexion = sqlite3.connect("hotel.db")
    cursor = conexion.cursor()
    cursor.execute(
        """ CREATE TABLE IF NOT EXISTS habitaciones(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        numero INTEGER,
        tipo TEXT,
        estado TEXT,
        huesped TEXT) """
    )
    conexion.commit()
    conexion.close()


inicializar_db()


class HabitacionNueva(BaseModel):
    numero: int
    tipo: str


@app.post("/Registrar_habitacion")
def registrar_habitacion(habitacion: HabitacionNueva):
    print("Registrando Habitacion")
    conexion = sqlite3.connect("hotel.db")
    cursor = conexion.cursor()
    cursor.execute(
        "INSERT INTO habitaciones (numero,tipo,estado,huesped) VALUES(?,?,'Libre','Nadie')",
        (habitacion.numero, habitacion.tipo),
    )
    conexion.commit()
    conexion.close()
    return {"mensaje": "Habitacion Registrada"}


@app.get("/ver_habitaciones")
def ver_disponible(solo_libre: int = None):
    conexion = sqlite3.connect("hotel.db")
    cursor = conexion.cursor()
    if solo_libre == 1:
        cursor.execute("SELECT * FROM habitaciones WHERE estado = 'Libre'")
    else:
        cursor.execute("SELECT * FROM habitaciones")
    resultado = cursor.fetchall()
    conexion.close()
    return resultado


@app.put("/habitaciones/{numero}/chekin")
def chekin(numero: int, cliente: str):
    conexion = sqlite3.connect("hotel.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT estado FROM habitaciones WHERE numero = ?", (numero,))
    resultado = cursor.fetchone()
    if resultado is None:
        conexion.close()
        raise HTTPException(status_code=404, detail="Esa habitacion no existe")
    estado_actual = resultado[0]
    if estado_actual == "ocupada":
        conexion.close()
        raise HTTPException(
            status_code=400, detail="La habitacion ya esta ocupada/sucia"
        )
    sql = "UPDATE habitaciones SET estado = 'ocupada', huesped = ? WHERE numero =?"
    cursor.execute(sql, (cliente, numero))
    conexion.commit()
    conexion.close()
    return {"mensaje": f"Check-in realizado para {cliente} en habitación {numero}"}


@app.put("/habitaciones/{numero}/checkout")
def chekin(numero: int):
    conexion = sqlite3.connect("hotel.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT estado FROM habitaciones WHERE numero = ?", (numero,))
    resultado = cursor.fetchone()
    if resultado is None:
        conexion.close()
        raise HTTPException(status_code=404, detail="Habitacion no encontrada")
    estado_actual = resultado[0]
    if estado_actual == "libre":
        conexion.close()
        raise HTTPException(status_code=400,detail="ERROR: La habitacion ya esta vacia")    
    sql = "UPDATE habitaciones SET estado = 'libre', huesped = 'nadie' WHERE numero = ?"
    cursor.execute(sql,(numero,))
    conexion.commit()
    conexion.close()
    return {"mensaje": f"Check-out listo. Habitación {numero} disponible nuevamente"}
