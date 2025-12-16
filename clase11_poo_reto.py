# agregar class


class Procesador:
    def __init__(self, marca, modelo):
        self.marca = marca
        self.modelo = modelo

    def mostrar_detalles(self):
        print(f"Soy un {self.marca} {self.modelo}")


proces1 = Procesador("intel", "i5 12700k")
proces2 = Procesador("amd", "5600g")

proces1.mostrar_detalles()
proces2.mostrar_detalles()
