import datetime # Para registrar fecha de inventario

# --- 1. DATOS INICIALES (Simulamos una Base de Datos) ---
inventario = {
    "RTX 4060": 320000,
    "Ryzen 5 5600X": 180000,
    "Monitor 144Hz": 210000,
    "Mouse Gamer": 35000
}

# --- 2. FUNCIONES (Nuestras Herramientas) ---

def mostrar_menu():
    print("\n--- SISTEMA DE GESTION PC ---")
    print("1. Ver Inventario")
    print("2. Agregar Nuevo Producto")
    print("3. Calcular Valor Total del Inventario")
    print("4. Salir")
    print("-----------------------------")

def ver_inventario():
    print(f"\n[Fecha consulta: {datetime.datetime.now()}]")
    print("--- LISTA DE PRODUCTOS ---")
    # Bucle FOR para recorrer el diccionario
    for producto, precio in inventario.items():
        print(f"- {producto}: ${precio}")

def agregar_producto():
    while True:
        nombre = input("\nNombre del producto (o 'cancelar'): ")
        if nombre == 'cancelar':
            break
        
        try:
            # TRY/EXCEPT para evitar errores si meten letras en el precio
            precio = int(input(f"Precio para '{nombre}': "))
            
            # Guardamos en el diccionario
            inventario[nombre] = precio
            print(f"¡Exito! {nombre} guardado correctamente.")
            break # Rompemos el bucle porque ya guardamos
            
        except ValueError:
            print("ERROR: El precio debe ser un numero entero. Intenta de nuevo.")

def calcular_total():
    suma_total = 0
    # Recorremos todos los precios y sumamos
    for precio in inventario.values():
        suma_total = suma_total + precio
    
    print(f"\n$$$ VALOR TOTAL EN BODEGA: ${suma_total} $$$")

# --- 3. BLOQUE PRINCIPAL (Main Loop) ---
# Aquí empieza a correr el programa de verdad

while True:
    mostrar_menu()
    
    opcion = input("Elige una opcion (1-4): ")
    
    if opcion == "1":
        ver_inventario()
    elif opcion == "2":
        agregar_producto()
    elif opcion == "3":
        calcular_total()
    elif opcion == "4":
        print("Cerrando sistema... ¡Hasta luego!")
        break
    else:
        print("Opcion no valida, intenta de nuevo.")