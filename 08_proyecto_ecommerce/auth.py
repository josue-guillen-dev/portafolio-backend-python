from passlib.context import CryptContext

# Configuramos la encriptación
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Función para ENCRIPTAR (Crear Hash)
def obtener_password_hash(password):
    return pwd_context.hash(password)

# Función para VERIFICAR (Login)
def verificar_password(password_plana, password_encriptada):
    return pwd_context.verify(password_plana, password_encriptada)