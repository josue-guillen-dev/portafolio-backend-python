# --- CLASE 6: MANEJO DE ERRORES (TRY / EXCEPT) ---
# Los programas fallan. Si un usuario ingresa texto en vez de numero,
# el programa explota (ValueError). 
# Para evitar que se cierre, usamos try/except.

print("--- INICIO DEL PROGRAMA ---")

while True:
    try:
        # 1. Intentamos (TRY) hacer algo peligroso
        precio = int(input("Ingresa el precio del producto: "))
        
        # Si la linea de arriba funciona, el codigo sigue aqui:
        print(f"Guardado. El precio es ${precio}")
        break # Rompemos el bucle porque si funciono

    except ValueError:
        # 2. Si ocurre un error especifico (ValueError), saltamos aqui.
        # El programa NO se cierra, solo muestra este mensaje y repite el bucle.
        print("ERROR: Amigo, escribiste letras. Por favor ingresa solo numeros.")

print("--- FIN DEL PROGRAMA ---")