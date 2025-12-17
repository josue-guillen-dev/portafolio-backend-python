from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from passlib.context import CryptContext
import sqlite3
import datetime

app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def inicializar_db():
    conexion = sqlite3.connect("billetera.db")
    cursor = conexion.cursor()
    cursor.execute(
        """ CREATE TABLE IF NOT EXISTS usuarios(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE,
        password TEXT,
        saldo INTEGER) """
    )
    cursor.execute(
        """ CREATE TABLE IF NOT EXISTS transacciones(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        origen_id TEXT,
        destino_id TEXT,
        monto INTEGER,
        fecha TEXT) """
    )
    conexion.commit()
    conexion.close()


inicializar_db()


class Usuario(BaseModel):
    email: str
    password: str
    saldo: int


class Transacciones(BaseModel):
    origen_id: int
    destino_id: int
    monto: int
    password_origen: str


@app.post("/registro")
def registro(usuario: Usuario):
    usuario_encriptado = pwd_context.hash(usuario.password)

    try:
        conexion = sqlite3.connect("billetera.db")
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO usuarios (email,password,saldo) VALUES (?,?,?)",
            (usuario.email, usuario_encriptado, 1000),
        )
        user_id = cursor.lastrowid
        conexion.commit()
        conexion.close()
        return {"mensaje": "Usuario creado", "id": user_id, "saldo_inicial": 1000}
    except sqlite3.IntegrityError:
        return {"error": "El email ya existe"}


@app.post("/login")
def login(usuario: Usuario):
    conexion = sqlite3.connect("billetera.db")
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT id,password, saldo FROM usuarios WHERE email = ?", (usuario.email,)
    )
    resultado = cursor.fetchone()
    conexion.close()

    if resultado is None:
        raise HTTPException(status_code=404, detail="Email no Existe")
    id_guardado = resultado[0]
    pass_guardada = resultado[1]
    saldo_actual = resultado[2]
    if pwd_context.verify(usuario.password, pass_guardada):
        return {"mensaje": "Login exitoso", "id": id_guardado, "tu_saldo": saldo_actual}
    else:
        raise HTTPException(status_code=400, detail="Contraseña incorrecta")


@app.post("/transferir")
def transferir_dinero(datos: Transacciones):
    conexion = sqlite3.connect("billetera.db")
    cursor = conexion.cursor()

    # --- VALIDACION 1: EL ORIGEN ---
    # Buscamos la contraseña y el saldo del usuario que quiere pagar
    cursor.execute(
        "SELECT password, saldo FROM usuarios WHERE id = ?", (datos.origen_id,)
    )
    usuario_origen = cursor.fetchone()

    # A. ¿Existe el usuario?
    if usuario_origen is None:
        # Cierra y lanza error 404
        conexion.close()
        raise HTTPException(status_code=404, detail="Usuario origen no encrontrado")

    # B. ¿La contraseña es correcta? (Usa pwd_context.verify)
    pass_guardada = usuario_origen[0]
    if not pwd_context.verify(datos.password_origen, pass_guardada):
        # Cierra y lanza error 400 "Contraseña incorrecta"
        conexion.close()
        raise HTTPException(status_code=400, detail="Contrasena de origen incorrecta")

    # C. ¿Tiene saldo suficiente?
    saldo_actual = usuario_origen[1]
    if saldo_actual < datos.monto:
        # Cierra y lanza error 400 "Saldo insuficiente"
        conexion.close()
        raise HTTPException(status_code=400, detail="saldo insuficiente")

    # --- VALIDACION 2: EL DESTINO ---
    # Buscamos si existe el usuario que recibe
    cursor.execute("SELECT id FROM usuarios WHERE id = ?", (datos.destino_id,))
    usuario_destino = cursor.fetchone()
    if usuario_destino is None:
        conexion.close()
        # Si es None, lanza error 404 "Destinatario no existe"
        raise HTTPException(status_code=404, detail="ID no existe")

    # --- ACCION: MOVER EL DINERO ---

    # 1. Restar al origen
    # SQL: UPDATE usuarios SET saldo = saldo - ? WHERE id = ?
    try:
        cursor.execute(
            "UPDATE usuarios SET saldo = saldo - ? WHERE id = ?",
            (datos.monto, datos.origen_id),
        )
        # 2. Sumar al destino
        # SQL: UPDATE usuarios SET saldo = saldo + ? WHERE id = ?
        cursor.execute(
            "UPDATE usuarios SET saldo = saldo + ? WHERE id = ?",
            (datos.monto, datos.destino_id),
        )

        # 3. Guardar en historial (Opcional por ahora, pero recomendado)
        # INSERT INTO transacciones ...
        fecha_hoy = str(datetime.date.today())
        cursor.execute(
            "INSERT INTO transacciones (origen_id, destino_id, monto, fecha) VALUES (?,?,?,?)",
            (datos.origen_id, datos.destino_id, datos.monto, fecha_hoy),
        )
        historial_tranf = {
            "mensaje": "tranferencia exitosa",
            "datos_transferencia": {
                "id_origen": datos.origen_id,
                "id_destino": datos.destino_id,
                "monto": datos.monto,
                "fecha": fecha_hoy,
            },
        }
        conexion.commit()
        conexion.close()
        return historial_tranf

    except Exception as e:
        conexion.close()
        raise HTTPException(status_code=500, detail=f"Error en la transacción: {e}")
