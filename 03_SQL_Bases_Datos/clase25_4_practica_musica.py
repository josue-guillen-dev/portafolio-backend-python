import sqlite3

conexion = sqlite3.connect("musica.db")
cursor = conexion.cursor()

cursor.execute("PRAGMA foreign_keys = ON;")

cursor.execute(
    """ CREATE TABLE IF NOT EXISTS artistas(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT,
    genero TEXT) """
)

cursor.execute(
    """ CREATE TABLE IF NOT EXISTS canciones(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT,
    duracion TEXT,
    artista_id INTEGER,
    FOREIGN KEY (artista_id) REFERENCES artistas(id)) """
)

try:
    print("Ingresando artista")
    cursor.execute(
        "INSERT INTO artistas (nombre,genero) VALUES ('daddy yankee','regueton')"
    )
    id_artista = cursor.lastrowid

    print("ingresando canciones")
    canciones_artista = [
        ("gasolina", "3:20", id_artista),
        ("llamada de emergencia", "3:20", id_artista),
    ]
    cursor.executemany(
        "INSERT INTO canciones (titulo, duracion, artista_id) VALUES (?,?,?)",
        canciones_artista,
    )

    print("Canciones guardadas.")

    conexion.commit()

except sqlite3.IntegrityError as e:
    print(f"🛑 ERROR DE INTEGRIDAD: {e}")
    print("No puedes crear un post para un usuario que no existe.")


cursor.execute(
    "SELECT canciones.titulo, artistas.nombre FROM canciones INNER JOIN artistas ON canciones.artista_id = artistas.id"
)
resultado = cursor.fetchall()
print("\n--- TIMELINE DE LA CANCION ---")
for fila in resultado:
    print(f"Cancion: {fila[0]} - Artista: {fila[1]}")

conexion.close()
