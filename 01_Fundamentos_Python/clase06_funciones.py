# --- CLASE 6: FUNCIONES (DEF) ---
# Una función es como crear tu propio comando personalizado.
# Sirve para no repetir código y tener todo ordenado.

# EJEMPLO 1: Una función simple que saluda
def saludar(nombre):
    print(f"Hola {nombre}, bienvenido al sistema.")

# EJEMPLO 2: Una función que hace calculos y DEVUELVE (return) un valor
def calcular_precio_final(precio_neto):
    # 1. Calculamos el IVA (19% en Chile)
    iva = precio_neto * 0.19
    
    # 2. Sumamos
    total = precio_neto + iva
    
    # 3. 'return' es clave: devuelve el resultado final hacia afuera
    return total

# --- ZONA DE PRUEBAS (Main) ---
print("--- INICIO DEL PROGRAMA ---")

# Usamos la funcion 1
saludar("Jotrexx")

# Usamos la funcion 2
precio_sin_iva = int(input("Ingresa el precio NETO del producto: "))

# AQUI llamamos a la función y guardamos lo que devuelve en una variable
precio_con_iva = calcular_precio_final(precio_sin_iva)

print(f"El precio final a pagar es: ${precio_con_iva}")