import sqlite3

conexion = sqlite3.connect("supermercado.db")
cursor = conexion.cursor()

cursor.execute("PRAGMA foreign_keys = ON;")

cursor.execute(
    """ CREATE TABLE IF NOT EXISTS categorias(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT) """
)
cursor.execute(
    """ CREATE TABLE IF NOT EXISTS productos(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT,
    precio INTEGER,
    categoria_id INTEGER,
    FOREIGN KEY (categoria_id) REFERENCES categorias(id)) """
)

try:
    print("Ingresando categoria")
    cursor.execute("INSERT INTO categorias (nombre) VALUES ('Electronica')")
    id_electronica = cursor.lastrowid #hacerlo por separado para varias

    cursor.execute("INSERT INTO categorias (nombre) VALUES ('frutas')")
    id_frutas = cursor.lastrowid #hacerlo por separado para varias
    print("Ingresando producto")
    productos = [
        ("televisor", "2200", id_electronica),
        ("radio", "1000", id_electronica),
    ]
    frutas = [("Manzana", "120", id_frutas), ("Pera", "120", id_frutas)]
    cursor.executemany(
        "INSERT INTO productos (nombre,precio,categoria_id) VALUES (?,?,?)", productos
    )
    cursor.executemany(
        "INSERT INTO productos (nombre,precio,categoria_id) VALUES (?,?,?)", frutas
    )
    conexion.commit()

except sqlite3.IntegrityError as e:
    print(f"🛑 ERROR DE INTEGRIDAD: {e}")
    print("No puedes crear un post para un usuario que no existe.")

cursor.execute(
    "SELECT productos.nombre, categorias.nombre FROM productos INNER JOIN categorias ON productos.categoria_id = categorias.id"
)

resultado = cursor.fetchall()

for fila in resultado:
    print(f"Producto: {fila[0]} - Seccion: {fila[1]}")
