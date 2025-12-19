# Esto es una LISTA (se usa corchetes [])
componentes = ["RTX 4060", "Ryzen 5", "RAM 16GB", "SSD 1TB"]

# En programacion, se empieza a contar desde CERO
print("El primer componente es:", componentes[0]) 
print("El segundo componente es:", componentes[1])

# Podemos agregar cosas nuevas a la lista con .append()
print("Agregando una Fuente de Poder...")
componentes.append("Fuente 600W")

print("Ahora el inventario es:", componentes[3])

print("--------------------------------------------------")
componentes = ["RTX 4060", "Ryzen 5", "RAM 16GB", "SSD 1TB", "Fuente 600W", "Gabinete"]

print("--- LISTA DE PRECIOS ---")

# La variable "producto" se inventa en ese momento
# y va tomando el valor de cada cosa en la lista, una por una.
for producto in componentes:
    print(f"OFERTA Llevese hoy su: {producto}")

print("--- FIN DE LISTA ---")