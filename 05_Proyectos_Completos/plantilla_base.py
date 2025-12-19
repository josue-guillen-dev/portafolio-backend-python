# Traemos FastAPI (para la web), Pydantic (para validar datos),
# Passlib (para seguridad) y SQLite (para la base de datos).
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from passlib.context import CryptContext
import sqlite3

# Definimos el nombre del archivo.
# Si mañana haces un proyecto de "Farmacia", solo cambias este nombre aquí.
NOMBRE_DB = "mi_proyecto.db"

app = FastAPI()
# Configuramos la encriptación una sola vez aquí para no repetirlo.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def ejecutar_sql(sql: str, datos: tuple = (), fetch_one=False, fetch_all=False):
    # 1. Conecta al nombre de base de datos que definimos arriba
    conexion = sqlite3.connect(NOMBRE_DB)
    cursor = conexion.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")  # Siempre activa relaciones

    # 2. Ejecuta la orden que le mandes
    cursor.execute(sql, datos)

    resultado = None

    # 3. Si pediste datos (SELECT), los guarda en 'resultado'
    if fetch_one:
        resultado = cursor.fetchone()
    elif fetch_all:
        resultado = cursor.fetchall()
    else:
        # 4. Si no es lectura (INSERT/UPDATE), guarda los cambios
        conexion.commit()

    # 5. Cierra y entrega el resultado
    conexion.close()
    return resultado


def inicializar_db():
    # Solo escribimos la orden SQL
    sql = """
    CREATE TABLE IF NOT EXISTS usuarios(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """
    # Y usamos nuestra función mágica para ejecutarla
    ejecutar_sql(sql)


# La llamamos al iniciar para que cree la tabla si no existe
inicializar_db()


class UsuarioModelo(BaseModel):
    username: str
    password: str


@app.post("/registro")
def registro(usuario: UsuarioModelo):
    # 1. Encriptamos la clave (NUNCA guardar texto plano)
    password_hash = pwd_context.hash(usuario.password)

    try:
        # 2. Preparamos la orden SQL
        sql = "INSERT INTO usuarios (username, password) VALUES (?, ?)"

        # 3. Ejecutamos usando nuestra función mágica
        # Ella se encarga de conectar, ejecutar, commit y cerrar.
        ejecutar_sql(sql, (usuario.username, password_hash))

        return {"mensaje": "Usuario registrado exitosamente"}

    except sqlite3.IntegrityError:
        # Si el usuario ya existe, lanzamos error 400
        raise HTTPException(status_code=400, detail="El usuario ya existe")


@app.post("/login")
def login(usuario: UsuarioModelo):
    # 1. Buscamos la contraseña encriptada del usuario
    sql = "SELECT password FROM usuarios WHERE username = ?"

    # Usamos fetch_one=True porque esperamos UN solo resultado
    resultado = ejecutar_sql(sql, (usuario.username,), fetch_one=True)

    # 2. Si no encontramos nada (resultado es None), el usuario no existe
    if not resultado:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # 3. Si existe, sacamos la contraseña encriptada de la tupla
    password_guardada = resultado[0]

    # 4. Verificamos: ¿La clave que escribió coincide con la encriptada?
    if pwd_context.verify(usuario.password, password_guardada):
        return {"mensaje": "Login Exitoso ✅"}
    else:
        raise HTTPException(status_code=400, detail="Contraseña Incorrecta ❌")
