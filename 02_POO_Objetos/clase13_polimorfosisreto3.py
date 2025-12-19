class Empleado:
    def __init__(self, nombre, sueldo_base):
        self.nombre = nombre
        self.sueldo_base = sueldo_base

    def calcular_pago(self):
        return self.sueldo_base

    def mostrar_detalle(self):
        print(f"Empleado {self.nombre} - sueldo: ${self.sueldo_base}")


class Programador(Empleado):
    def __init__(self, nombre, sueldo_base, bono_proyecto):
        super().__init__(nombre, sueldo_base)
        self.bono_proyecto = bono_proyecto
    def calcular_pago(self):
        return self.sueldo_base + self.bono_proyecto
    
class Gerente(Empleado):
    def __init__(self, nombre, sueldo_base, bono_gestion):
        super().__init__(nombre, sueldo_base)
        self.bono_gestion = bono_gestion
    def calcular_pago(self):
        return self.sueldo_base + self.bono_gestion
    
nomina = [
    Empleado("Ana", 550000),
    Programador("Beto", 1100000, 100000),
    Gerente("Carla", 1500000, 500000)
]

for trabajador in nomina:
    trabajador.mostrar_detalle()
    
    pago = trabajador.calcular_pago()
    print(f"Pago final a recibir: ${pago}")
    