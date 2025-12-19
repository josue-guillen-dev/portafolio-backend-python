# ==========================================
# DESAFIO 1: El Portero de la Discoteca (Condicionales)
# ==========================================
# 1. Pide al usuario su edad con input() y conviertelo a numero (int).
# 2. Si es mayor o igual a 18, imprime "Bienvenido a la fiesta".
# 3. Si es menor, imprime "Lo siento, vuelve cuando seas grande".

print("\n--- DESAFIO 1 ---")
# TU CODIGO AQUI:
edad_user = int(input("Ingresa tu edad: "))
if edad_user >= 18:
    print("Bienvenido a la fiesta")
else:
    print("Lo siento, vuelve cuando seas grande")

print("---------------------------------------------")
# ==========================================
# DESAFIO 2: La Lista de Compras (Bucles y Listas)
# ==========================================
# 1. Crea una lista vacia llamada 'carrito'.
# 2. Usa un bucle 'for' que se repita 3 veces (usa range(3)).
# 3. En cada vuelta, pide al usuario que escriba un producto.
# 4. Agrega ese producto a la lista 'carrito'.
# 5. Al final, imprime: "Tu carrito tiene: [lista]"

print("\n--- DESAFIO 2 ---")
# TU CODIGO AQUI:
carrito = []
for i in range(3):
    producto = input("ingresa un producto: ")
    carrito.append(producto)
print(f"tu carrito tiene: {carrito}")


# ==========================================
# DESAFIO 3: Convertidor de Moneda (Funciones)
# ==========================================
# 1. Crea una funcion llamada 'convertir_a_dolares' que reciba 'pesos'.
# 2. Dentro, calcula los dolares (dividiendo pesos por 950).
# 3. Retorna el resultado.
# 4. Fuera de la funcion, pide al usuario un monto en pesos, llama a tu funcion
#    e imprime el resultado.

print("\n--- DESAFIO 3 ---")


# TU CODIGO AQUI:
def convertir_a_dolares(pesos):
    dolares = pesos / 950
    return dolares


pesos = int(input("Ingrese monto en pesos: "))
dolares = convertir_a_dolares(pesos)
print(f"tu cantidad de dolares al cambio son {dolares}")


# ==========================================
# DESAFIO 4: El Buscador de Stock (Diccionarios y Errores)
# ==========================================
stock = {"Monitor": 5, "Mouse": 10, "Teclado": 0}

# 1. Pide al usuario que ingrese el nombre de un producto a buscar.
# 2. Intenta imprimir la cantidad de stock de ese producto.
# 3. Si el producto NO existe (KeyError), captura el error e imprime "Producto no encontrado".

print("\n--- DESAFIO 4 ---")
# TU CODIGO AQUI:
while True:
    try:
        busqueda = input("Ingrese producto a buscar: ")
        print(f"cantidad en stock: {stock[busqueda]}")
        break
    except KeyError:
        print("Producto no encontrado")
# ==========================================
# DESAFIO 5: Par o Impar (Modulo %)
# ==========================================
# 1. Pide al usuario un numero entero.
# 2. Si el numero es Par (su resto al dividir por 2 es 0), imprime "Es Par".
# 3. Si no, imprime "Es Impar".

print("\n--- DESAFIO 5 ---")
# TU CODIGO AQUI:
par = int(input("Ingrese un numero entero: "))
if par % 2 == 0:
    print("Es par")
else:
    print("Es Impar")

print("\n--- FIN DEL EXAMEN ---")
