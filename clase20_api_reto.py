"""Vas a construir el sistema para una biblioteca pequeña. Este ejercicio probará tu capacidad para manejar Estados (Disponible / Prestado).

Crea un archivo llamado practica_biblioteca.py."""

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import sqlite3

app = FastAPI()


def inicializar_db():
    conexion = sqlite3.connect("libros_biblioteca.db")
    cursor = conexion.cursor()
    cursor.execute(
        """ CREATE TABLE IF NOT EXISTS libros(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT,
        autor TEXT,
        estado TEXT) """
    )
    conexion.commit()
    conexion.close()


inicializar_db()


class LibroEntrada(BaseModel):
    titulo: str
    autor: str


@app.post("/Registrar_libro")
def registrar_libro(libro: LibroEntrada):
    print("Registrando libro")
    conexion = sqlite3.connect("libros_biblioteca.db")
    cursor = conexion.cursor()
    cursor.execute(
        "INSERT INTO libros (titulo, autor, estado) VALUES (?,?,'Disponible')",
        (libro.titulo, libro.autor),
    )
    conexion.commit()
    conexion.close()
    return {"mensaje": "libro Registrado"}


@app.get("/buscar libro")
def buscar_libro(autor: str = Query(None)):
    conexion = sqlite3.connect("libros_biblioteca.db")
    cursor = conexion.cursor()
    if autor:
        cursor.execute("SELECT * FROM libros WHERE autor LIKE ?", (f"%{autor}%",))
    else:
        cursor.execute("SELECT * FROM libros")
    filas = cursor.fetchall()

    libros = []
    for fila in filas:
        libro = {"id": fila[0], "titulo": fila[1], "autor": fila[2], "estado": fila[3]}
        libros.append(libro)
    return libros


@app.put("/libros/{id_libro}/prestar")
def prestar_libro(id_libro: int):
    conexion = sqlite3.connect("libros_biblioteca.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT estado FROM libros WHERE id = ?", (id_libro,))
    resultado = cursor.fetchone()
    conexion.commit()
    if resultado is None:
        conexion.close()
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    estado_actual = resultado[0]
    if estado_actual == "Prestado":
        conexion.close()
        raise HTTPException(status_code=404, detail="El libro ya esta ocupado")
    cursor.execute("UPDATE libros SET estado = 'Prestado' WHERE id = ?", (id_libro,))
    conexion.commit()
    conexion.close()
    return {"mensaje": "Libro prestado correctamente"}

@app.put("/libros/{id_libro}/devolver")
def devolver_libro(id_libro: int):
    conexion = sqlite3.connect("libros_biblioteca.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT estado FROM libros WHERE id = ?", (id_libro,))
    resultado = cursor.fetchone()
    conexion.commit()
    if resultado is None:
        conexion.close()
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    estado_actual = resultado[0]
    if estado_actual == "Disponible":
        conexion.close()
        raise HTTPException(status_code=404, detail="El libro Esta en la biblioteca")
    cursor.execute("UPDATE libros SET estado = 'Disponible' WHERE id = ?", (id_libro,))
    conexion.commit()
    conexion.close()
    return {"mensaje": "Libro Regresado a la biblioteca"}


@app.delete("/libros/{id_libro}")
def borrar_libro(id_libro: int):
    conexion = sqlite3.connect("libros_biblioteca.db")
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM libros WHERE id = ?", (id_libro,))
    conexion.commit()
    if cursor.rowcount == 0:
        conexion.close()
        raise HTTPException(status_code=404, detail="El libro no existe")
    conexion.close()
    return {"mensaje": "Libro eliminado exitosamente"}
