import sqlite3


def inicializar_db():
    conexion = sqlite3.connect("agenda.db")
    cursor = conexion.cursor()

    cursor.execute(
        """ 
            CREATE TABLE IF NOT EXISTS contactos(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT,
                telefono TEXT,
                email TEXT)
                """
    )
    conexion.commit()
    conexion.close()


def agregar_contacto():
    print("--- CONTACTO NUEVO ---")
    nombre = input("Ingrese nombre de contacto: ")
    telefono = input("Ingrese tu numero de telefono: ")
    email = input("Ingrese tu email: ")

    conexion = sqlite3.connect("agenda.db")
    cursor = conexion.cursor()
    cursor.execute(
        "INSERT INTO contactos (nombre,telefono,email) VALUES(?,?,?)",
        (nombre, telefono, email)
    )
    conexion.commit()
    conexion.close()


def ver_contacto():
    print("--- LISTA DE CONTACTOS ---")

    conexion = sqlite3.connect("agenda.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM contactos")
    lista = cursor.fetchall()
    if len(lista) == 0:
        print("lista de contactos vacia")
    else:
        for a in lista:
            print(f"ID: {a[0]} | {a[1]} | {a[2]} | {a[3]}")
    conexion.close()


def buscar_contacto():
    buscar = input("Ingrese contacto a buscar: ")
    conexion = sqlite3.connect("agenda.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM contactos WHERE nombre LIKE ?",(f"%{buscar}%",))
    resultado = cursor.fetchall()
    if resultado:
        for fila in resultado:
            print(fila)
    else:
        print("No encontrado")
    conexion.close()


def eliminar_contacto():
    id = int(input("Ingrese el id del usuario que quiere borrar: "))
    conexion = sqlite3.connect("agenda.db")
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM contactos WHERE id = ?",(id,))
    if cursor.rowcount > 0:
        print("Contacto Borrado")
    else:
        print("Ese ID no existe")
    conexion.commit()
    conexion.close()

inicializar_db()

while True:
    print("\n--- MENU PRINCIPAL ---")
    print("1. Nuevo Contacto")
    print("2. Ver Contactos")
    print("3. Buscar Por Nombre")
    print("4. Eliminar por ID")
    print("5. Salir")
    try:
        opcion = int(input("Elija una opcion: "))
        if opcion == 1:
            agregar_contacto()
            print("Contacto Guardado")
        elif opcion ==2:
            ver_contacto()
        elif opcion == 3:
            buscar_contacto()
        elif opcion == 4:
            eliminar_contacto()
        elif opcion == 5:
            print("Cerrando Sistema")
            break
    except ValueError:
        print("Ingrese una opcion valida")