from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI()


def inicializar_db():
    conexion = sqlite3.connect("tarea.db")
    cursor = conexion.cursor()
    cursor.execute(
        """ CREATE TABLE IF NOT EXISTS tareas(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT,
        descripcion TEXT,
        completada INTEGER) """
    )
    conexion.commit()
    conexion.close()


inicializar_db()


class NuevaTarea(BaseModel):
    titulo: str
    descripcion: str
    completada: int


@app.post("/crear_tareas")
def recibir_tarea(tarea: NuevaTarea):
    print("Tarea Creada")
    conexion = sqlite3.connect("tarea.db")
    cursor = conexion.cursor()
    cursor.execute(
        "INSERT INTO tareas (titulo,descripcion,completada) VALUES (?,?,?)",
        (tarea.titulo, tarea.descripcion, tarea.completada),
    )
    conexion.commit()
    conexion.close()
    return {f"tarea {tarea.descripcion} Guardada"}


@app.get("/ver_tareas")
def revisar_tareas(ver_compleatada: int = None):
    conexion = sqlite3.connect("tarea.db")
    cursor = conexion.cursor()
    if ver_compleatada is None:
        cursor.execute("SELECT * FROM tareas")
    elif ver_compleatada == 1:
        cursor.execute("SELECT * FROM tareas WHERE completada = 1")
    elif ver_compleatada == 0:
        cursor.execute("SELECT * FROM tareas WHERE completada = 0")
    else:
        cursor.execute("SELECT * FROM tareas")

    resultados = cursor.fetchall()
    conexion.close()

    lista_final = []
    for tareas in resultados:
        item = {
            "id": tareas[0],
            "titulo": tareas[1],
            "descripcion": tareas[2],
            "completada": tareas[3],
        }
        lista_final.append(item)
    return lista_final


@app.delete("/borrar_tareas/{id_tarea}")
def borrar_tarea(id_tarea: int):
    conexion = sqlite3.connect("tarea.db")
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM tareas WHERE id = ?", (id_tarea,))
    conexion.commit()
    if cursor.rowcount == 0:
        conexion.close()
        raise HTTPException(status_code=404, detail="Tarea no encontrado")
    conexion.close()
    return {f"Tarea {id_tarea} eliminada"}


@app.put("/actualizar_tareas/{id_tarea}")
def actualizar_tarea(id_tarea: int):
    conexion = sqlite3.connect("tarea.db")
    cursor = conexion.cursor()
    cursor.execute("UPDATE tareas SET completada = 1 WHERE id = ?", (id_tarea,))
    conexion.commit()
    if cursor.rowcount == 0:
        conexion.close()
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    conexion.close()
    return {f"Tarea {id_tarea} marcada como completada"}
