# Pedimos el precio NETO
precio = int(input("Ingresa el precio NETO de la GPU: "))

# Ahora si podemos multiplicar (Calculamos IVA 19% en Chile)
iva = precio * 0.19
precio_final = precio + iva

print(f"El IVA es: {iva}")
print(f"Total a pagar: {precio_final}")

while True:
    mi_dinero = int(input("Cuanto dinero tienes en tu bolsillo: "))
    if mi_dinero == 0:
        print("Adios")
        break
    if mi_dinero >= 50000:
        print("Te alcanza para la memoria RAM")
    else:
        print("Sigue ahorrando")
