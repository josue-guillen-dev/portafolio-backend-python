import sqlite3

NOMBRE_DB = "sistema_modular.db"


def ejecutar_sql(sql: str, datos: tuple = (), fetch_one=False, fetch_all=False):
    conexion = sqlite3.connect(NOMBRE_DB)
    cursor = conexion.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    cursor.execute(sql, datos)
    resultado = None
    if fetch_one:
        resultado = cursor.fetchone()
    elif fetch_all:
        resultado = cursor.fetchall()
    else:
        conexion.commit()
        conexion.close()
    return resultado


def inicializar_db():
    sql_usuarios = """ CREATE TABLE IF NOT EXISTS usuarios(
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        username TEXT UNIQUE, 
        password TEXT ) """
    ejecutar_sql(sql_usuarios)
    print("Base de datos inicializada correctamente.")
