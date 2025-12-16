class Ticket:
    def __init__(self, id, usuario, descripcion):
        self.id = id
        self.usuario = usuario
        self.descripcion = descripcion
        self.status = "Pendiente"

    def mostrar_info(self):
        print(f"Ticket #{self.id}: {self.usuario} reporta: {self.descripcion}")

    def resolver(self):
        print("Resolviendo ticket generico")
        self.status = "Resuelto"

class Bug(Ticket):
    def __init__(self, id, usuario, descripcion, severidad):
        super().__init__(id, usuario, descripcion)
        self.severidad = severidad

    def resolver(self):
        print(f"Corrigiendo bug {self.severidad} en el codigo")
        self.status = "Corregido" 

class Featured(Ticket):
    def __init__(self, id, usuario, descripcion, area):
        super().__init__(id, usuario, descripcion)
        self.area = area
    def resolver(self):
        print(f"--> Implementando nueva funcion para el area de {self.area}...")
        self.status= "Implementado"
    
class SistemaSoporte:
    def __init__(self):
        self.tickets = []
        
    def crear_ticket(self, ticket):
        self.tickets.append(ticket)
        print(f"[Sistema] Ticket #{ticket.id} recibido.")
        
    def procesar_todo(self):
        print("\n--- INICIANDO PROCESAMIENTO ---")
        
        for tarea in self.tickets:
            tarea.mostrar_info()
            tarea.resolver()
            print(f"Estado Final: {tarea.status}")
            print("-----------------")

mi_sistema = SistemaSoporte()

bug_critico = Bug(1,"juan","pantalla azul","CRITICO")
nueva_idea = Featured(2,"juan","agregar modo oscuro","Diseno")
bug_leve = Bug(3,"juan","pantalla negra","LEVE")

mi_sistema.crear_ticket(bug_critico)
mi_sistema.crear_ticket(nueva_idea)
mi_sistema.crear_ticket(bug_leve)

mi_sistema.procesar_todo()