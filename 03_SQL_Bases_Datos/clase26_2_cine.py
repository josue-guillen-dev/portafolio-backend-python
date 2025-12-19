import sqlite3

conexion = sqlite3.connect("cine.db")
cursor = conexion.cursor()

cursor.execute("PRAGMA foreign_keys = ON;")

cursor.execute(""" CREATE TABLE IF NOT EXISTS peliculas(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT,
    anio INTEGER) """)
cursor.execute(""" CREATE TABLE IF NOT EXISTS actores(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT)""")
cursor.execute(""" CREATE TABLE IF NOT EXISTS elenco(
    pelicula_id INTEGER,
    actor_id INTEGER,
    FOREIGN KEY (pelicula_id) REFERENCES peliculas(id),
    FOREIGN KEY (actor_id) REFERENCES actores(id)) """)

try:
    cursor.execute("INSERT INTO actores (nombre) VALUES ('Leonardo Dicaprio')")
    id_dicaprio = cursor.lastrowid
    cursor.execute("INSERT INTO actores (nombre) VALUES ('Kate Winslet')")
    id_kate = cursor.lastrowid
    cursor.execute("INSERT INTO actores (nombre) VALUES ('Cillian Murphy')")
    id_cillian = cursor.lastrowid
    
    cursor.execute("INSERT INTO peliculas (titulo) VALUES ('Titanic')")
    id_titanic = cursor.lastrowid
    cursor.execute("INSERT INTO peliculas (titulo) VALUES ('Origen')")
    id_origen = cursor.lastrowid
    
    elenco = [
        (id_dicaprio, id_titanic),
        (id_kate, id_titanic),
        (id_dicaprio, id_origen),
        (id_cillian, id_origen),
    ]
    
    cursor.executemany("INSERT INTO elenco (actor_id, pelicula_id) VALUES (?,?)", elenco,)
    
    conexion.commit()
    
except sqlite3.IntegrityError as e:
    print(f"🛑 ERROR DE INTEGRIDAD: {e}")
    
cursor.execute(""" SELECT peliculas.titulo, actores.nombre
            FROM elenco
            INNER JOIN peliculas ON elenco.pelicula_id = peliculas.id
            INNER JOIN actores ON elenco.actor_id = actores.id""")    

resultado = cursor.fetchall()

for fila in resultado:
    print(f"Pelicula: {fila[0]} - Actor: {fila[1]}")
    
conexion.close()