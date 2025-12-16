# --- CLASE 09: HERENCIA ---

# 1. CLASE PADRE (La base general)
class Componente:
    def __init__(self, marca, precio):
        self.marca = marca
        self.precio = precio
    
    def mostrar_info(self):
        print(f"Producto: {self.marca} - Valor: ${self.precio}")

# 2. CLASE HIJA (Hereda de Componente)
# Ponemos (Componente) entre parentesis para decir "Soy hijo de este"
class TarjetaGrafica(Componente):
    def __init__(self, marca, precio, vram):
        # super().__init__ llama al constructor del Padre para que haga el trabajo sucio
        super().__init__(marca, precio) 
        self.vram = vram # Solo agregamos lo nuevo
    
    def renderizar(self):
        print(f"La {self.marca} esta renderizando graficos 3D...")

# --- PRUEBA ---
# Creamos una GPU. Fíjate que le pasamos marca y precio, 
# ¡aunque la clase TarjetaGrafica no tiene self.marca escrito explicitamente!
mi_gpu = TarjetaGrafica("Nvidia", 400000, 8)

# Usamos un metodo que HEREDO del padre
mi_gpu.mostrar_info() 

# Usamos un metodo propio
mi_gpu.renderizar()