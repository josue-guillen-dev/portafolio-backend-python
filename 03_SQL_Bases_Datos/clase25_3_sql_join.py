import sqlite3

print("--- LEYENDO BLOG (CON JOIN) ---")

conexion = sqlite3.connect("blog.db")
cursor = conexion.cursor()

# LA GRAN CONSULTA
# Traduccción:
# "Selecciona el titulo (de posts) y el nombre (de usuarios)
# DE la tabla posts
# UNIENDO (JOIN) con la tabla usuarios
# DONDE el autor_id (del post) coincida con el id (del usuario)"

sql = """
    SELECT posts.titulo, usuarios.nombre
    FROM posts
    INNER JOIN usuarios ON posts.autor_id = usuarios.id
"""

cursor.execute(sql)
resultados = cursor.fetchall()

print("\n--- TIMELINE DEL BLOG ---")
for fila in resultados:
    # fila es: ("Mi primer post", "Juan")
    print(f"📰 '{fila[0]}' - Escrito por: {fila[1]}")

conexion.close()
