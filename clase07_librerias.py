# --- CLASE 7: IMPORTAR LIBRERIAS (MODULES) ---
# "No reinventes la rueda". Python tiene herramientas listas para usar.
# Solo tienes que decir "import nombre_herramienta"

import random   # Herramienta para cosas al azar
import datetime # Herramienta para fechas y horas

print("--- SISTEMA DE VENTAS ---")

# EJEMPLO 1: Usando RANDOM
# Imagina que quieres simular si hay stock o no (50% probabilidad)
# random.choice elige uno al azar de la lista
estado = random.choice(["Disponible", "Agotado", "En Transito"])

print(f"Estado del producto: {estado}")

# EJEMPLO 2: Usando RANDOM con numeros
# Generar un numero de descuento aleatorio entre 5 y 20
descuento = random.randint(5, 20)
print(f"¡Felicidades! Tienes un {descuento}% de descuento hoy.")

# EJEMPLO 3: Usando DATETIME
# Queremos saber exactamente cuando ocurrio la venta
# datetime.datetime.now() te da la fecha y hora actual de tu PC
fecha_actual = datetime.datetime.now()

print("---------------------------")
print(f"Comprobante generado el: {fecha_actual}")
print("---------------------------")