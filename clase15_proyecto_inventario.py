import sqlite3


def inicializar_db():
    conexion = sqlite3.connect("inventario_maestro.db")
    cursor = conexion.cursor()

    cursor.execute(
        """ 
    CREATE TABLE IF NOT EXISTS productos(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        precio INTEGER,
        stock INTEGER
        )
    """
    )

    conexion.commit()
    conexion.close()  # Cerramos despues de crear


def agregar_producto():
    print("\n--- NUEVO PRODUCTO ---")
    nombre = input("Ingrese nombre de producto a registrar: ")
    try:
        precio = int(input("Ingrese precio del producto a registar: "))
        stock = int(input("Ingrese stock del producto a registrar: "))
    except ValueError:
        print("ERROR: Precio y Stock debe ser numerico")
        return  # Salimos de la funcion si hay error

    # 2. Conectamos solo para guardar
    conexion = sqlite3.connect("inventario_maestro.db")
    cursor = conexion.cursor()
    cursor.execute(
        "INSERT INTO productos (nombre,precio,stock) VALUES (?,?,?)",
        (nombre, precio, stock),
    )
    conexion.commit()
    conexion.close()
    print("Producto Guardado\n")


def ver_producto():
    print("\n--- INVENTARIO ---")
    conexion = sqlite3.connect("inventario_maestro.db")
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM productos")
    lista = cursor.fetchall()
    if len(lista) == 0:
        print("El invetario esta vacio")
    else:
        for p in lista:
            print(f"ID:{p[0]} | {p[1]} | ${p[2]} | {p[3]}")
    conexion.close()


# --- PROGRAMA PRINCIPAL ---

inicializar_db()  # Nos aseguramos que la tabla exista antes de empezar

while True:
    print("\n--- MENU PRINCIPAL ---")
    print("1-Ver Inventario")
    print("2-Agregar Nuevo")
    print("3-Salir")

    try:
        opcion = int(input("Elija una opcion: "))

        if opcion == 1:
            ver_producto()
            pass
        elif opcion == 2:
            agregar_producto()
            pass
        elif opcion == 3:
            print("Cerrando sistema")
            break
    except ValueError:
        print("Porfavor ingrese un numero")
