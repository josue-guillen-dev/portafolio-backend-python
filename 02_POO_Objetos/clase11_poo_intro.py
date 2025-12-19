# --- CLASE 08: INTRODUCCION A POO ---
# Una CLASE es un molde para crear objetos.

class TarjetaGrafica:
    
    # 1. EL CONSTRUCTOR (__init__)
    # Esta funcion especial se ejecuta AUTOMATICAMENTE cuando creas una nueva tarjeta.
    # Sirve para configurar los datos iniciales.
    # 'self' significa "yo mismo" (se refiere a la tarjeta especifica que esta naciendo).
    def __init__(self, nombre, vram):
        self.nombre = nombre   # Guardo el nombre en mi memoria interna
        self.vram = vram       # Guardo la vram en mi memoria interna
        self.encendida = False # Por defecto, nacen apagadas

    # 2. METODOS (Acciones)
    # Son funciones que solo funcionan dentro de este objeto
    def encender(self):
        self.encendida = True
        print(f"--> {self.nombre}: Ventiladores al 100%... ¡ONLINE!")

    def info(self):
        # Usamos self.nombre para acceder a MIS datos
        print(f"[INFO] Soy una {self.nombre} con {self.vram}GB de video.")

# --- ZONA DE PRUEBAS ---
print("--- FABRICANDO TARJETAS ---")

# Creamos (Instanciamos) dos objetos distintos usando el mismo molde
gpu1 = TarjetaGrafica("RTX 4060", 8)
gpu2 = TarjetaGrafica("RX 7900", 24)

# Cada una tiene sus propios datos guardados dentro
gpu1.info()
gpu2.info()

print("\n--- PROBANDO ACCIONES ---")
# Podemos mandar a encender una, y la otra sigue apagada
gpu1.encender()

# Podemos acceder a los datos internos con el punto (.)
print(f"¿La {gpu2.nombre} esta encendida? {gpu2.encendida}")


print("-----------------------------------")
class TarjetaGrafica:
    def __init__(self, nombre):
        self.nombre = nombre

# 1. Creamos dos tarjetas IGUALES usando el mismo molde
gpu1 = TarjetaGrafica("RTX 4060")
gpu2 = TarjetaGrafica("RTX 4060")

print(f"Original GPU 1: {gpu1.nombre}")
print(f"Original GPU 2: {gpu2.nombre}")

# 2. CAMBIAMOS solo la GPU 2
print("\n--- Modificando GPU 2... ---")
gpu2.nombre = "GTX 1650 (La cambie)"

# 3. Vemos que paso
print(f"Ahora GPU 1 es: {gpu1.nombre}") # ¿Cambio?
print(f"Ahora GPU 2 es: {gpu2.nombre}")