# Diccionario: { "Producto" : Precio }
catalogo = {"RTX 4060": 320000, "Ryzen 5": 180000, "RAM 16GB": 45000}

# Para saber el precio, NO usamos numeros [0], usamos el NOMBRE
print("El precio de la Ryzen 5 es:", catalogo["Ryzen 5"])
print("El precio de la RAM 16GB:", catalogo["RAM 16GB"])
# print(catalogo["Ryzen 5"])

# Llego mercaderia nueva: Agregamos un Teclado
catalogo["Teclado Mecanico"] = 40000
print("-------------------")
print("Catalogo actualizado", catalogo)


while True:
    nuevo_producto = input("Ingresa nuevo producto (o escribe 'salir'): ")
    if nuevo_producto == "salir":
        print("saliendo de agregar producto")
        break
    precio = int(input("Ingresa precio nuevo producto: "))
    catalogo[nuevo_producto] = precio
print("Catalogo actualizado", catalogo)
