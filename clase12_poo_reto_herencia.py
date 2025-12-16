class Componente:
    def __init__(self, marca, precio):
        self.marca = marca
        self.precio = precio

    def mostrar_info(self):
        print(f"Producto: {self.marca} - Valor: ${self.precio}")


class Procesador(Componente):
    def __init__(self, marca, precio, nucleos):
        super().__init__(marca, precio)
        self.nucleos = nucleos


process1 = Procesador("Ryzen 5", 180000, "6 Nucleos")

process1.mostrar_info()
