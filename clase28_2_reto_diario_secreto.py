from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from passlib.context import CryptContext
import sqlite3

app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def inicializar_db():
    conexion = sqlite3.connect("usuarios_1.db")
    cursor = conexion.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    cursor.execute(
        """ CREATE TABLE IF NOT EXISTS usuarios(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT)"""
    )
    cursor.execute(
        """ CREATE TABLE IF NOT EXISTS entradas(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT,
        texto TEXT,
        user_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES usuarios(id))"""
    )
    conexion.commit()
    conexion.close()


inicializar_db()


class Usuarios(BaseModel):
    username: str
    password: str


class Entradas(BaseModel):
    titulo: str
    texto: str


@app.post("/registro")
def registrar_user(usuario: Usuarios):
    password_encriptada = pwd_context.hash(usuario.password)
    conexion = sqlite3.connect("usuarios_1.db")
    cursor = conexion.cursor()
    cursor.execute(
        "INSERT INTO usuarios (username, password) VALUES (?,?)",
        (usuario.username, password_encriptada),
    )
    user_id = cursor.lastrowid
    conexion.commit()
    conexion.close()
    return {"mensaje": f"Usuario Guardado id:{user_id}"}


@app.post("/login")
def login(usuario: Usuarios):
    conexion = sqlite3.connect("usuarios_1.db")
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT password FROM usuarios WHERE username = ?", (usuario.username,)
    )
    resultado = cursor.fetchone()
    conexion.close()

    if resultado is None:
        raise HTTPException(status_code=404, detail="Usuario no Encontrado")
    password_guardada = resultado[0]
    if pwd_context.verify(usuario.password, password_guardada):
        return {"mensaje": f"Bienvenido {usuario.username} Acceso concedido"}
    else:
        raise HTTPException(status_code=404, detail="Contrasena Incorrecta")


@app.post("/usuarios/{user_id}/entradas")
def post_user(user_id: int, post: Entradas):
    conexion = sqlite3.connect("usuarios_1.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT id FROM usuarios WHERE id = ?", (user_id,))
    usuario = cursor.fetchone()
    if usuario is None:
        conexion.close()
        raise HTTPException(status_code=404, detail="ID no encontrado")

    cursor.execute(
        "INSERT INTO entradas (titulo,texto, user_id) VALUES (?,?,?)",
        (post.titulo, post.texto, user_id),
    )
    conexion.commit()
    conexion.close()
    return {"mensaje": f"Post Guardado en tu diario"}


@app.get("/usuarios/{user_id}/entradas")
def ver_usuarios(user_id: int):
    conexion = sqlite3.connect("usuarios_1.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT id, username FROM usuarios WHERE id = ?", (user_id,))
    usuario = cursor.fetchone()

    if usuario is None:
        conexion.close()
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    cursor.execute("SELECT titulo,texto FROM entradas WHERE user_id = ?", (user_id,))
    posts = cursor.fetchall()
    conexion.close()

    lista_post = []
    for post in posts:
        lista_post.append({"titulo": post[0], "texto": post[1]})
    return {"id": usuario[0],"username": usuario[1],"total_posts":len(lista_post), "posts": lista_post}

