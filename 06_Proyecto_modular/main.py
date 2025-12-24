from fastapi import FastAPI, HTTPException
from passlib.context import CryptContext
import sqlite3
from database import ejecutar_sql, inicializar_db
from models import UsuarioModelo

app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

inicializar_db()


@app.get("/")
def home():
    return {"mensaje": "API Modular funcionando"}


@app.post("/registro")
def registro(usuario: UsuarioModelo):
    password_hash = pwd_context.hash(usuario.password)
    try:
        sql = "INSERT INTO usuarios (username, password) VALUES (?, ?)"
        ejecutar_sql(sql, (usuario.username, password_hash))
        return {"mensaje": "Usuario registrado exitosamente"}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="El usuario ya existe")


@app.post("/login")
def login(usuario: UsuarioModelo):
    sql = "SELECT password FROM usuarios WHERE username = ?"
    resultado = ejecutar_sql(sql, (usuario.username,), fetch_one=True)
    if not resultado:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    password_guardada = resultado[0]
    if pwd_context.verify(usuario.password, password_guardada):
        return {"mensaje": "Login Exitoso"}
    else:
        raise HTTPException(status_code=400, detail="Contraseña Incorrecta")
