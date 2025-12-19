import sqlite3

conexion = sqlite3.connect("blog.db")
cursor = conexion.cursor()
# ¡IMPORTANTE! Activar restricciones de llave foranea siempre
cursor.execute("PRAGMA foreign_keys = ON;")

try:
    # 1. Creamos al Padre (Usuario)
    print("Creando usuario Juan...")
    cursor.execute(
        "INSERT INTO usuarios (nombre, email) VALUES ('Juan', 'juan@email.com')"
    )

    # Obtenemos el ID del usuario recién creado
    id_juan = cursor.lastrowid
    print(f"Juan tiene el ID: {id_juan}")

    # 2. Creamos Hijos (Posts) vinculados a Juan
    print("Creando posts para Juan...")
    posts_de_juan = [
        ("Mi primer post", "Hola mundo", id_juan),
        ("Python es genial", "Aprendiendo SQL Relacional", id_juan),
    ]
    cursor.executemany(
        "INSERT INTO posts (titulo, contenido, autor_id) VALUES (?,?,?)", posts_de_juan
    )
    print("Posts guardados.")

    # 3. EL EXPERIMENTO (Descomenta esto para ver el error)
    # print("Intentando crear post para un fantasma...")
    # cursor.execute("INSERT INTO posts (titulo, contenido, autor_id) VALUES (?,?,?)",
    #                ("Post Ilegal", "Texto", 999))

    conexion.commit()

except sqlite3.IntegrityError as e:
    print(f"🛑 ERROR DE INTEGRIDAD: {e}")
    print("No puedes crear un post para un usuario que no existe.")

finally:
    conexion.close()
