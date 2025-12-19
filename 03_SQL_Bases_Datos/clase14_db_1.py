import sqlite3

print("--- BUSCADOR DE PRODUCTOS ---")

# 1. CONECTAMOS a la base de datos existente
# Fíjate que no creamos tabla ni insertamos nada, solo leemos.
conexion = sqlite3.connect("tienda.db")
cursor = conexion.cursor()

# 2. VERIFICAR QUE HAY DATOS
print("Productos disponibles actualmente:")
cursor.execute("SELECT * FROM productos")
todos = cursor.fetchall()

for p in todos:
    # p es una tupla: (id, nombre, precio, stock)
    print(f"#{p[0]} - {p[1]} (${p[2]}) - Stock: {p[3]}")
    
print("-----------------------------")
    
# 3. FILTRADO CON 'WHERE'
# Vamos a pedirle al usuario un presupuesto maximo
presupuesto = input("que productos buscas: ")
print(f"\nBuscando productos por menos de ${presupuesto}...")

# LA CONSULTA SQL CON FILTRO
# El signo ? es un placeholder (espacio seguro) que Python rellena con tu variable

sql = "SELECT * FROM productos WHERE nombre = ?"
cursor.execute(sql, (presupuesto,))

resultados = cursor.fetchall()

if len(resultados) > 0:
    for p in resultados:
        print(f"--> ¡ENCONTRADO!: {p[1]} a ${p[2]}")
else:
    print("No hay nada tan barato :(")

# 4. CERRAR
conexion.close()