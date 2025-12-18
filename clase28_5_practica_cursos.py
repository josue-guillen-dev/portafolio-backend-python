from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from passlib.context import CryptContext
import sqlite3
import datetime

app = FastAPI()

pwd_password = CryptContext(schemes=["bcrypt"], deprecated="auto")


def inicializar_db():
    conexion = sqlite3.connect("practica_curso.db")
    cursor = conexion.cursor()
    cursor.execute(
        """ CREATE TABLE IF NOT EXISTS usuarios(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT,
        password TEXT,
        es_profesor INTEGER) """
    )
    cursor.execute(
        """ CREATE TABLE IF NOT EXISTS cursos(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT,
        precio INTEGER,
        profesor_id INTEGER,
        FOREIGN KEY (profesor_id) REFERENCES usuarios(es_profesor)) """
    )
    cursor.execute(
        """ CREATE TABLE IF NOT EXISTS inscripciones(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        curso_id INTEGER,
        fecha TEXT) """
    )
    conexion.commit()
    conexion.close()


inicializar_db()


class Usuarios(BaseModel):
    email: str
    password: str
    es_profesor: int = 0


class Cursos(BaseModel):
    titulo: str
    precio: int
    profesor_id: int


class Inscripciones(BaseModel):
    curso_id: int
    user_id: int


@app.post("/registro")
def registrar(usuario: Usuarios):
    password_encriptada = pwd_password.hash(usuario.password)
    try:
        conexion = sqlite3.connect("practica_curso.db")
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO usuarios (email,password,es_profesor) VALUES (?,?,?)",
            (usuario.email, password_encriptada, usuario.es_profesor),
        )
        conexion.commit()
        conexion.close()
        return {"mensaje": "Usuario Registrado"}
    except sqlite3.IntegrityError:
        return {"error": "Email ya existe"}


@app.post("/login")
def login(usuario: Usuarios):
    conexion = sqlite3.connect("practica_curso.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT password FROM usuarios WHERE email = ?", (usuario.email,))
    user = cursor.fetchone()
    conexion.close()
    if user is None:
        conexion.close()
        raise HTTPException(status_code=404, detail="email no existe")

    if pwd_password.verify(usuario.password, user[0]):
        return {"mensaje": "inicio de sesion exitoso"}
    else:
        conexion.close()
        raise HTTPException(status_code=400, detail="Contrasena Incorrecta")


@app.post("/cursos")
def cursos(curso: Cursos):
    conexion = sqlite3.connect("practica_curso.db")
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT es_profesor FROM usuarios WHERE id = ?", (curso.profesor_id,)
    )
    user = cursor.fetchone()
    if user is None:
        conexion.close()
        raise HTTPException(status_code=404, detail="Usuario no existe")
    es_profe = user[0]
    if es_profe == 0:
        conexion.close()
        raise HTTPException(status_code=403, detail="No tiene permiso")
    cursor.execute(
        "INSERT INTO cursos (titulo,precio,profesor_id) VALUES (?,?,?)",
        (curso.titulo, curso.precio, curso.profesor_id),
    )

    conexion.commit()
    conexion.close()
    return {"mensaje": "curso guardado"}


@app.post("/inscripciones")
def inscripciones(user: Inscripciones):
    conexion = sqlite3.connect("practica_curso.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT id FROM cursos WHERE id = ?", (user.curso_id,))
    curso = cursor.fetchone()
    if curso is None:
        conexion.close()
        raise HTTPException(status_code=404, detail="Curso no existe")
    cursor.execute(
        "SELECT * FROM inscripciones WHERE user_id = ? AND curso_id = ?",
        (user.user_id, user.curso_id),
    )
    existe = cursor.fetchone()
    if existe:
        conexion.close()
        raise HTTPException(status_code=400, detail="Ya tienes este curso")
    fecha = str(datetime)
    cursor.execute(
        "INSERT INTO inscripciones (user_id,curso_id,fecha) VALUES (?,?,?)",
        (user.user_id, user.curso_id,fecha),
    )
    conexion.commit()
    conexion.close()
    return {"mensaje": "Inscripción realizada con éxito"}


@app.get("/usuarios/{user_id}/cursos")
def ver_cursos(user_id: int):
    conexion = sqlite3.connect("practica_curso.db")
    cursor = conexion.cursor()
    cursor.execute(
        """SELECT cursos.titulo 
        FROM inscripciones
        INNER JOIN cursos ON inscripciones.curso_id = cursos.id
        WHERE inscripciones.user_id = ?""",
        (user_id,),
    )
    curso = cursor.fetchall()
    conexion.close()
    if not curso:
        return {"usuario": user_id, "cursos": []}
    lista_cursos = [fila[0] for fila in curso]

    return {"Usuario": user_id, "cursos": lista_cursos}
