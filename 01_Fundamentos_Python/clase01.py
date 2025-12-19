# Esto es una variable (una caja para guardar datos)
nombre_gpu = "RTX 4060"
precio = 320000
stock = False  # True significa Verdadero (Sí hay stock)

# Vamos a imprimir un mensaje usando esos datos (f-string)
print(f"Producto: {nombre_gpu}")
print(f"Valor: ${precio}")

if stock:
    print("Esta disponible para comprar")
else:
    print("Agotado :(")
    
