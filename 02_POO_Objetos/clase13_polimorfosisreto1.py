# --- PRACTICA POO: SISTEMA BANCARIO ---
# INSTRUCCIONES:
# Completa las clases siguiendo las reglas del negocio.

print("\n--- INICIO DEL SISTEMA BANCARIO ---")

# ==========================================
# DESAFIO 1: La Clase Cuenta
# ==========================================
# 1. Crea una clase 'Cuenta'.
# 2. En el __init__, debe recibir 'titular' y 'saldo' inicial.
# 3. Crea un metodo 'depositar(monto)' que sume al saldo.
# 4. Crea un metodo 'retirar(monto)'. 
#    - OJO: Solo puede retirar si tiene saldo suficiente.
#    - Si no tiene, imprime "Fondos insuficientes".
# 5. Crea un metodo 'mostrar_saldo()' que imprima "Titular: [nombre] - Saldo: $[saldo]"

# TU CODIGO AQUI:
class Cuenta:
    def __init__(self, titular, saldo):
        self.titular = titular
        self.saldo = saldo
    def depositar(self, monto):
        self.saldo += monto
        print(f"Depositado ${monto}. Saldo actual ${self.saldo}")
    def retirar(self, monto):
        if self.saldo >= monto:
            self.saldo -= monto
            print(f"Retirando ${monto}. Saldo actual ${self.saldo}")
            return True
        else:
            print("Fondos insuficientes")
            return False
    def mostrar_saldo(self):
        print(f"titular: {self.titular} - Saldo ${self.saldo}")




# ==========================================
# DESAFIO 2: Herencia (Cuenta Joven)
# ==========================================
# 1. Crea una clase 'CuentaJoven' que herede de 'Cuenta'.
# 2. Esta cuenta REGALA $10.000 extra al crearse (en el __init__).
#    (Pista: Llama a super().__init__ y luego suma 10000 al self.saldo)
# 3. Tiene un metodo extra 'bonificacion()' que suma un 5% al saldo actual.

# TU CODIGO AQUI:

class CuentaJoven(Cuenta):
    def __init__(self, titular, saldo):
        super().__init__(titular, saldo)
        self.saldo += 10000
    def bonificacion(self):
        self.saldo = self.saldo* 1.05
        print(f"¡Felicidades! Ganaste una bonificación.")

# ==========================================
# DESAFIO 3: Interaccion entre Objetos
# ==========================================
# ESTO ES UN RETO DE LOGICA:
# Crea una funcion SUELTA (fuera de las clases) llamada 'transferir'.
# Debe recibir: (origen, destino, monto).
# 1. Saca dinero de la cuenta 'origen' (usando su metodo retirar).
# 2. Si el retiro funcionó (pista: tendras que verificar el saldo antes),
#    deposita ese dinero en la cuenta 'destino'.

def transferir(origen, destino, monto):
    # TU CODIGO AQUI:
    if origen.retirar(monto):
        destino.depositar(monto)
        print("Transferencia Exitosa")
    else:
        print("Transferencia fallida: Saldo insuficiente")

# --- ZONA DE PRUEBAS ---
print("\n--- PRUEBAS ---")

# 1. Prueba Desafio 1
print("1. Creando cuenta normal...")
cuenta1 = Cuenta("Juan Perez", 50000)
cuenta1.depositar(20000)
cuenta1.retirar(10000)
cuenta1.mostrar_saldo() # Deberia ser 60000

# 2. Prueba Desafio 2
print("\n2. Creando cuenta joven...")
cuenta2 = CuentaJoven("Maria Gomez", 20000) # Deberia empezar con 30000 por el regalo
cuenta2.bonificacion()
cuenta2.mostrar_saldo()

# 3. Prueba Desafio 3
print("\n3. Probando transferencia...")
# Juan le manda 5000 a Maria
transferir(cuenta1, cuenta2, 5000)

print("\nSaldos Finales:")
cuenta1.mostrar_saldo() # Deberia tener 55000
cuenta2.mostrar_saldo() # Deberia haber recibido los 5000