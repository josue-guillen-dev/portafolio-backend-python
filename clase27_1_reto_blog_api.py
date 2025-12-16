from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import sqlite3

app = FastAPI()


def inicializar_db():
    conexion = sqlite3.connect("blog.db")
    cursor = conexion.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    cursor.execute(
        """ CREATE TABLE IF NOT EXISTS usuarios(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        email TEXT) """
    )
    cursor.execute(
        """ CREATE TABLE IF NOT EXISTS posts(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT,
        contenido TEXT,
        user_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES usuarios(id)) """
    )
    conexion.commit()
    conexion.close()


inicializar_db()


class CrearUsuario(BaseModel):
    nombre: str
    email: str


class PostCrear(BaseModel):
    titulo: str
    contenido: str


@app.post("/usuarios")
def guardar_usuarios(guardar: CrearUsuario):
    conexion = sqlite3.connect("blog.db")
    cursor = conexion.cursor()
    cursor.execute(
        "INSERT INTO usuarios (nombre, email) VALUES (?,?)",
        (guardar.nombre, guardar.email),
    )
    conexion.commit()
    user_id = cursor.lastrowid
    conexion.close()
    return {"mensaje": "Usuario Creado", "ID": user_id}


@app.post("/usuarios/{user_id}/posts")
def crear_posts_usuario(user_id: int, posts: PostCrear):
    conexion = sqlite3.connect("blog.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT id FROM usuarios WHERE id = ?", (user_id,))
    usuario = cursor.fetchone()
    if usuario is None:
        conexion.close()
        raise HTTPException(status_code=404, detail="Usuario no existe")

    cursor.execute(
        "INSERT INTO posts (titulo,contenido,user_id) VALUES (?,?,?)",
        (posts.titulo, posts.contenido, user_id),
    )
    conexion.commit()
    post_id = cursor.lastrowid
    conexion.close()
    return {"mensaje": "Post creado", "post_id": post_id, "user_id": user_id}


@app.get("/usuarios/{user_id}")
def ver_user_post(user_id: int):
    conexion = sqlite3.connect("blog.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE user_id = ?", (user_id,))
    usuario = cursor.fetchone()

    if usuario is None:
        conexion.close()
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    cursor.execute("SELECT titulo,contenido FROM posts WHERE user_id = ?", (user_id,))
    posts = cursor.fetchall()

    conexion.close()
    lista_post = []
    for post in posts:
        lista_post.append({"titulo": post[0], "contenido": post[1]})
    respuesta = {
        "id": usuario[0],
        "nombre": usuario[1],
        "email": usuario[2],
        "posts": lista_post,
    }
    return respuesta
