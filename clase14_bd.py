import sqlite3

print("--- SISTEMA DE TIENDA CON SQLITE ---")

# 1. CONEXION (Crea el archivo si no existe)
conexion = sqlite3.connect("tienda.db")
cursor = conexion.cursor()

# 2. CREAR TABLA
# Usamos """ para escribir en varias lineas
# INTEGER PRIMARY KEY AUTOINCREMENT hace que el ID se ponga solo (1, 2, 3...)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        precio INTEGER,
        stock INTEGER
    )
""")
print("Tabla 'productos' verificada.")

# 3. INSERTAR DATOS
# Vamos a guardar 3 productos de ejemplo
datos_nuevos = [
    ("Teclado Mecanico", 45000, 10),
    ("Mouse Gamer", 25000, 5),
    ("Monitor 24 pulg", 120000, 2)
]

# executemany es un truco para guardar una lista de golpe
# Los signos ? son espacios vacios que se llenan con los datos
cursor.executemany("INSERT INTO productos (nombre, precio, stock) VALUES (?, ?, ?)", datos_nuevos)

# 4. GUARDAR CAMBIOS (Commit)
conexion.commit()
print("Datos guardados correctamente.")

# 5. LEER DATOS (Para confirmar que funciono)
print("\n--- INVENTARIO ACTUAL ---")
cursor.execute("SELECT * FROM productos")
productos = cursor.fetchall()

for p in productos:
    print(p) # Veras algo como (1, 'Teclado', 45000, 10)

# 6. CERRAR
conexion.close()