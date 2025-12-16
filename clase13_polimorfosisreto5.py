class Vehiculo:
    def __init__(self, marca, modelo):
        self.marca = marca
        self.modelo = modelo

    def arrancar(self):
        print(f"El {self.marca} {self.modelo} esta arrancando")


class Auto(Vehiculo):
    def __init__(self, marca, modelo, puertas):
        super().__init__(marca, modelo)
        self.puertas = puertas

    def arrancar(self):
        print(f"El auto {self.marca} ruge con motor V8. Vrooooom")

    def abrir_maleta(self):
        print("Abriendo la maleta para guardar el equipaje")


class Moto(Vehiculo):
    def __init__(self, marca, modelo, cilindrada):
        super().__init__(marca, modelo)
        self.cilindrada = cilindrada

    def arrancar(self):
        print(f"La Moto {self.marca} enciende. ratatata")

    def hacer_wheelie(self):
        print("Haciendo un caballito")


class Garaje:
    def __init__(self):
        self.estacionamiento = []

    def estacionar(self, vehiculo):
        self.estacionamiento.append(vehiculo)
        print(f"Guardando {vehiculo.marca} {vehiculo.modelo} en el garaje")

    def sacar_todo(self):
        for item in self.estacionamiento:
            item.arrancar()

            if isinstance(item, Auto):
                item.abrir_maleta()

mi_garaje = Garaje()

mi_auto = Auto("Toyota", "Yaris", 4)
mi_moto = Moto("Ducati", "Monster", "900cc")

mi_garaje.estacionar(mi_auto)
mi_garaje.estacionar(mi_moto)

mi_garaje.sacar_todo()