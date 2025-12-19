from passlib.context import CryptContext

# 1. Configuramos la maquina de encriptar
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 2. Tu contraseña secreta
mi_clave = "hola123"

# 3. ¡Magia! La convertimos en hash
clave_encriptada = pwd_context.hash(mi_clave)

print(f"Clave original: {mi_clave}")
print(f"Clave guardada: {clave_encriptada}")

# 4. Verificar (Simular Login)
# Probamos si "hola123" coincide con el hash raro
es_correcta = pwd_context.verify("hola123", clave_encriptada)
print(f"¿La clave es correcta? {es_correcta}")