class Personajes:
    def __init__(self, nombre, vida, fuerza):
        self.nombre = nombre
        self.vida = vida
        self.fuerza = fuerza

    def recibir_dano(self, cantidad):
        self.vida -= cantidad
        if self.vida <= 0:
            print(f"{self.nombre} a sido Derrotado")
        else:
            print(f"{self.nombre} le queda {self.vida} de vida")

    def atacar(self, enemigo):
        print(f"{self.nombre} ataca a {enemigo.nombre}")
        enemigo.recibir_dano(self.fuerza)


class Guerrero(Personajes):
    def __init__(self, nombre, vida, fuerza, espada):
        super().__init__(nombre, vida, fuerza)
        self.espada = espada

    def atacar(self, enemigo):
        enemigo.recibir_dano(self.fuerza + self.espada)


class Mago(Personajes):
    def __init__(self, nombre, vida, fuerza, libro_hechizos):
        super().__init__(nombre, vida, fuerza)
        self.libro_hechizos = libro_hechizos

    def atacar(self, enemigo):
        enemigo.recibir_dano(self.fuerza + self.libro_hechizos)


guerrero1 = Guerrero("goku", 100, 35, espada=15)
guerrero2 = Mago("freezer", 100, 28, libro_hechizos=20)

while guerrero1.vida > 0 and guerrero2.vida > 0:

    guerrero1.atacar(guerrero2)
    if guerrero2.vida <= 0:
        break

    guerrero2.atacar(guerrero1)
    if guerrero1.vida <= 0:
        break

print("----FIN DE LA PELEA----")
