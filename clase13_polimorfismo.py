# --- CLASE 10: POLIMORFISMO ---

# 1. CLASE BASE (El Padre)
class Componente:
    def conectar(self):
        # Esta funcion es generica, solo para que los hijos la tengan
        print("Conectando dispositivo desconocido...")

# 2. CLASES HIJAS (Los Especialistas)
class TarjetaVideo(Componente):
    def conectar(self):
        # Aqui "sobreescribimos" la accion original
        print("--> GPU: Dando imagen al monitor por HDMI.")

class Teclado(Componente):
    def conectar(self):
        print("--> TECLADO: Encendiendo luces RGB. Listo para escribir.")

class DiscoDuro(Componente):
    def conectar(self):
        print("--> SSD: Girando disco. Cargando Windows...")

# --- PRUEBA MAESTRA (Polimorfismo en accion) ---

# Creamos una lista con componentes MEZCLADOS
# No importa que sean distintos, todos son "Componentes"
mis_piezas = [
    TarjetaVideo(),
    Teclado(),
    DiscoDuro(),
    TarjetaVideo() # Otra GPU mas
]

print("--- ENCENDIENDO EL PC ---")

# EL MAGICO BUCLE FOR
# Aqui esta el truco: Le damos la MISMA orden (.conectar) a todos.
# Python es inteligente y sabe cual version usar para cada uno.

for pieza in mis_piezas:
    pieza.conectar() 
    # Fíjate que no preguntamos "if es teclado..." ni "if es gpu..."