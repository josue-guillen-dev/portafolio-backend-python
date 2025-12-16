import sqlite3

conexion = sqlite3.connect("escuela_compleja.db")
cursor = conexion.cursor()

cursor.execute("PRAGMA foreign_keys = ON;")

cursor.execute(
    """ CREATE TABLE IF NOT EXISTS estudiantes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT) """
)
cursor.execute(
    """ CREATE TABLE IF NOT EXISTS cursos(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT) """
)
cursor.execute(
    """ CREATE TABLE IF NOT EXISTS inscripciones(
    estudiante_id INTEGER,
    curso_id INTEGER,
    FOREIGN KEY (estudiante_id) REFERENCES estudiantes(id),
    FOREIGN KEY (curso_id) REFERENCES cursos(id)) """
)

try:
    print("Ingresando estudiantes")
    cursor.execute("INSERT INTO estudiantes (nombre) VALUES ('Ana')")
    id_ana = cursor.lastrowid

    cursor.execute("INSERT INTO estudiantes (nombre) VALUES ('beto')")
    id_beto = cursor.lastrowid

    cursor.execute("INSERT INTO cursos (titulo) VALUES ('Python')")
    id_python = cursor.lastrowid

    cursor.execute("INSERT INTO cursos (titulo) VALUES ('Cocina')")
    id_cocina = cursor.lastrowid

    inscripciones = [(id_ana, id_python), (id_ana, id_cocina), (id_beto, id_cocina)]
    cursor.executemany(
        "INSERT INTO inscripciones (estudiante_id, curso_id) VALUES (?,?)",
        inscripciones,
    )
    print("Inscripciones guardadas correctamente.")

    conexion.commit()

except sqlite3.IntegrityError as e:
    print(f"🛑 ERROR DE INTEGRIDAD: {e}")
    print("No puedes crear un post para un usuario que no existe.")

cursor.execute(
    """ SELECT estudiantes.nombre, cursos.titulo 
    FROM inscripciones 
    INNER JOIN estudiantes ON inscripciones.estudiante_id = estudiantes.id INNER JOIN cursos ON inscripciones.curso_id = cursos.id """
)
resultado = cursor.fetchall()
for fila in resultado:
    print(f"Alumno: {fila[0]} - Curso: {fila[1]}")

conexion.close()
