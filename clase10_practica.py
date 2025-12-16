# --- PRACTICA REFORZADA FASE 1: LOGICA INTERMEDIA ---
# INSTRUCCIONES:
# Estos ejercicios simulan problemas reales de trabajo.
# Rellena el codigo donde dice "# TU CODIGO AQUI".

import random  # Necesario para el Desafio 5

print("\n--- INICIO DE LA PRACTICA ---")

# ==========================================
# DESAFIO 1: El Validador de Contraseñas (Strings)
# ==========================================
# Una contraseña es segura si tiene MAS de 6 caracteres.
# 1. Pide al usuario una contraseña.
# 2. Elimina los espacios en blanco al principio y final (usa .strip()).
# 3. Si la longitud (len) es mayor a 6, imprime "Contraseña Guardada".
# 4. Si no, imprime "Insegura: Debe tener mas de 6 letras".

print("\n--- DESAFIO 1 ---")
# TU CODIGO AQUI:

while True:
    contrasena = input("Ingresa una contrasena de 6 caracteres minimo: ").strip()
    if len(contrasena) > 6:
        print("Contrasena Guradada")
        break
    else:
        print("Insegura: Debe tener mas de 6 letras")


# ==========================================
# DESAFIO 2: Calculadora de Promedios (Bucles y Acumuladores)
# ==========================================
# Queremos saber el promedio de notas de un alumno.
# 1. Crea una lista vacia 'notas'.
# 2. Usa un bucle while True para pedir notas.
# 3. Si escribe 'fin', rompe el bucle.
# 4. Si es numero, guardalo en la lista (recuerda float() para decimales).
# 5. Al final, calcula el promedio (suma total / cantidad de notas) e imprimelo.
# PISTA: La funcion sum(lista) suma todo lo de adentro.

print("\n--- DESAFIO 2 ---")
# TU CODIGO AQUI:
notas = []
while True:
    pedir_notas = input("Ingrese notas del 1 al 20: ")
    if pedir_notas == "fin":
        break
    else:
        pedir_notas = int(pedir_notas)
        notas.append(pedir_notas)
if len(notas) > 0:
    promedio = sum(notas) / len(notas)
    print(f"El promedio total de las notas es: {promedio}")
else:
    print("No ingresaste ninguna nota")

# ==========================================
# DESAFIO 3: Base de Datos de Clientes (Listas de Diccionarios)
# ==========================================
# Esto es MUY comun en el trabajo real. Una lista de objetos.
clientes = [
    {"id": 1, "nombre": "Juan", "deuda": 0},
    {"id": 2, "nombre": "Maria", "deuda": 50000},
    {"id": 3, "nombre": "Pedro", "deuda": 12000},
]

# 1. Recorre la lista de clientes con un bucle for.
# 2. Si el cliente tiene deuda mayor a 0, imprime: "CLIENTE [Nombre] DEBE PAGAR".
# 3. Si la deuda es 0, no imprimas nada.

print("\n--- DESAFIO 3 ---")
# TU CODIGO AQUI:

for cliente in clientes:
    if cliente["deuda"] > 0:
        print(f"CLIENTE {cliente["nombre"]} DEBE PAGAR")


# ==========================================
# DESAFIO 4: El Formateador de Texto (Metodos de String)
# ==========================================
# A veces los usuarios escriben mal sus datos (todo minuscula, espacios extra).
# 1. Pide al usuario su "Nombre Completo".
# 2. Convierte lo que escribio a "Titulo" (Primera letra mayuscula de cada palabra).
#    Pista: Busca sobre el metodo .title()
# 3. Imprime "Nombre registrado: [nombre arreglado]"

print("\n--- DESAFIO 4 ---")
# TU CODIGO AQUI:

nombre_completo = input("Ingrese nombre completo: ")
nombre_arreglado = nombre_completo.title()
print(f"Nombre normal {nombre_completo}")
print(f"Nombre Arreglado {nombre_arreglado}")


# ==========================================
# DESAFIO 5: Adivina el Número (Logica y Random)
# ==========================================
# 1. Genera un numero secreto entre 1 y 10.
numero_secreto = random.randint(1, 10)

# 2. Pide al usuario que adivine el numero.
# 3. Si adivina, imprime "¡Ganaste!" y termina.
# 4. Si no, dile si el numero secreto es MAYOR o MENOR al que dijo.
# 5. Repite hasta que gane.

print("\n--- DESAFIO 5 ---")
# TU CODIGO AQUI:

while True:

    adivinar_numero = int(input("Adivina el numero que estoy pensando entre 1 y 10: "))
    if adivinar_numero == numero_secreto:
        print("Ganaste")
        break
    elif adivinar_numero < numero_secreto:
        print("Es un numero mayor")
    else:
        print("Es un numero menor")


print("\n--- FIN DE LA PRACTICA ---")
