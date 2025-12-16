from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import sqlite3

app = FastAPI()


def inicializar_db():
    conexion = sqlite3.connect("escuela.db")
    cursor = conexion.cursor()

    cursor.execute(
        """ CREATE TABLE IF NOT EXISTS alumnos(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        curso TEXT,
        promedio REAL) """
    )
    conexion.commit()
    conexion.close()


inicializar_db()


class AlumnoNuevo(BaseModel):
    nombre: str
    curso: str
    promedio: float


@app.post("/alumnos")
def guardar_alumno(alumno: AlumnoNuevo):
    conexion = sqlite3.connect("escuela.db")
    cursor = conexion.cursor()
    cursor.execute(
        "INSERT INTO alumnos (nombre,curso,promedio) VALUES (?,?,?)",
        (alumno.nombre, alumno.curso, alumno.promedio),
    )
    conexion.commit()
    conexion.close()
    return {"mensaje": "Alumno Matriculado"}


@app.get("/alumnos")
def ver_alumnos(curso: str = Query(None)):
    conexion = sqlite3.connect("escuela.db")
    cursor = conexion.cursor()

    if curso:
        cursor.execute("SELECT * FROM alumnos WHERE curso = ?", (curso,))
    else:
        cursor.execute("SELECT * FROM alumnos")
    resultado = cursor.fetchall()

    lista_alumnos = []
    for alumnos in resultado:
        lista_alumnos.append(
            {
                "id": alumnos[0],
                "nombre": alumnos[1],
                "curso": alumnos[2],
                "promedio": alumnos[3],
            }
        )
    conexion.close()
    return lista_alumnos

@app.put("/alumnos/{id_alumno}/corregir_nota")
def corregir_nota(id_alumno: int, nuevo_promedio: float = Query):
    conexion = sqlite3.connect("escuela.db")
    cursor = conexion.cursor()
    if nuevo_promedio < 1.0 or nuevo_promedio > 7.0:
        raise HTTPException(status_code=400, detail="Nota Invalida")
    else:
        cursor.execute("UPDATE alumnos SET promedio = ? WHERE id = ?",(nuevo_promedio,id_alumno,))
    conexion.commit()
    if cursor.rowcount == 0:
        conexion.close()
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
    conexion.close()
    return {"mensaje": f"Promedio Alumno ID: {id_alumno} actualizado"}
    
@app.delete("/alumnos/{id_alumno}")
def borrar_alumno(id_alumno: int):
    conexion = sqlite3.connect("escuela.db")
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM alumnos WHERE id = ?", (id_alumno,))
    if cursor.rowcount == 0:
        conexion.close()
        raise HTTPException(status_code=404, detail="alumno inexistente")
    conexion.commit()
    conexion.close()
    return {"mensaje": "Alumno Eliminado"}
    
    