from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import sqlite3
from passlib.context import CryptContext

app = FastAPI()


def inicializar_db():
    conexion = sqlite3.connect("usuarios.db")
    cursor = conexion.cursor()
    cursor.execute(
        """ CREATE TABLE IF NOT EXISTS usuario(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        password TEXT) """
    )
    conexion.commit()
    conexion.close()


inicializar_db()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Usuario(BaseModel):
    nombre: str
    password: str


@app.post("/registro")
def guardar_usuario(usuario: Usuario):
    password_encriptada = pwd_context.hash(usuario.password)
    conexion = sqlite3.connect("usuarios.db")
    cursor = conexion.cursor()
    cursor.execute(
        "INSERT INTO usuario (nombre,password) VALUES (?,?)",
        (usuario.nombre, password_encriptada),
    )
    
    conexion.commit()
    conexion.close()
    return {"mensaje": "Usuario Creado"}

# --- RUTA DE LOGIN ---
@app.post("/login")
def login(usuario: Usuario):
    conexion = sqlite3.connect("usuarios.db")
    cursor = conexion.cursor()
    
    # 1. Buscamos al usuario
    cursor.execute("SELECT password FROM usuario WHERE nombre = ?", (usuario.nombre,))
    resultado = cursor.fetchone()
    conexion.close()
    
    # 2. Si no existe
    if resultado is None:
        raise HTTPException(status_code=400, detail="Usuario incorrecto")
    
    # 3. Si existe, sacamos el hash guardado
    password_hash_guardada = resultado[0]
    
    # 4. Verificamos si la contraseña coincide
    if pwd_context.verify(usuario.password, password_hash_guardada):
        return {"mensaje": f"Bienvenido {usuario.nombre}, acceso concedido ✅"}
    else:
        raise HTTPException(status_code=400, detail="Contraseña incorrecta ❌")