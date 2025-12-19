class Componente:
    def __init__(self, nombre, precio, watts):
        self.nombre = nombre
        self.precio = precio
        self.watts = watts

    def mostrar(self):
        print(f"Pieza: {self.nombre} (${self.precio})-{self.watts}W")


class Ram(Componente):
    def __init__(self, nombre, precio, watts, capacidad_gb):
        super().__init__(nombre, precio, watts)
        self.capacidad_gb = capacidad_gb


class Cpu(Componente):
    def __init__(self, nombre, precio, watts, nucleos):
        super().__init__(nombre, precio, watts)
        self.nucleos = nucleos


class Gpu(Componente):
    def __init__(self, nombre, precio, watts, vram):
        super().__init__(nombre, precio, watts)
        self.vram = vram


class Computadora:
    def __init__(self):
        self.piezas = []

    def agregar_piezas(self, componente):
        self.piezas.append(componente)
        print(f"Agregando al gabinete {componente.nombre}")

    def mostrar_resumen(self):
        print("\n---- RESUMEN DEL PC")
        total_precio = 0
        total_watts = 0
        for pieza in self.piezas:
            pieza.mostrar()
            total_precio += pieza.precio
            total_watts += pieza.watts

        print("----------------------")
        print(f"PRECIO TOTAL: ${total_precio}")
        print(f"CONSUMO TOTAL: {total_watts}W")
        print("----------------------")
        
        if total_watts > 500:
            print("AVISO: Se necesita una fuente de 600 watts")
        else:
            print("ESTADO: funcionando con normalidad")
            
print("--- INICIANDO ARMADO DE PC ---")

mi_cpu = Cpu("Ryzen 5 5600g", 180000, 65, 6)
mi_ram = Ram("fury beast 16gb", 45000, 5, 16)
mi_gpu = Gpu("RTX 4060", 320000, 115, 8)
mi_ram2 = Ram("kiston 16gb",45000,5,16)

mi_pc = Computadora()

mi_pc.agregar_piezas(mi_cpu)
mi_pc.agregar_piezas(mi_ram)
mi_pc.agregar_piezas(mi_ram2)
mi_pc.agregar_piezas(mi_gpu)

mi_pc.mostrar_resumen()