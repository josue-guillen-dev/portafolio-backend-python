import sqlite3

# 1. Conectar a blog.db
conexion = sqlite3.connect("blog.db")
cursor = conexion.cursor()

# 2. Activar las Llaves Foraneas (En SQLite vienen apagadas por defecto)
cursor.execute("PRAGMA foreign_keys = ON;")

# 3. CREAR TABLA PADRE (Usuarios)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        email TEXT
    )
""")

# 4. CREAR TABLA HIJA (Posts)
# Aqui te toca a ti escribir la magia.
# Recuerda: FOREIGN KEY (autor_id) REFERENCES usuarios(id)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT,
        contenido TEXT,
        autor_id INTEGER,
        FOREIGN KEY (autor_id) REFERENCES usuarios(id)
    )
""")

conexion.commit()
conexion.close()
print("Tablas relacionadas creadas.")