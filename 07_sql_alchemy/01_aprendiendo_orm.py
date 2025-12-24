# 1. Importaciones de SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

# 2. Configuración (El Jefe)
# Creamos el motor. echo=True nos mostrará en consola el SQL que escribe por nosotros.
motor = create_engine("sqlite:///mi_primera_orm.db", echo=True)

# 3. La Base (El Molde Maestro)
Base = declarative_base()

# 4. Definimos la Tabla como una CLASE (Aquí está la magia)
class Usuario(Base):
    __tablename__ = "usuarios" # Nombre de la tabla en la BD
    
    # Definimos columnas como si fueran variables
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    edad = Column(Integer)

    # Esto es solo para que se vea bonito al imprimir
    def __repr__(self):
        return f"Usuario(id={self.id}, nombre={self.nombre}, edad={self.edad})"

# 5. CREAR LA BASE DE DATOS
# Esta linea le dice a SQLAlchemy: "Mira todas las clases que heredan de Base
# y crea las tablas correspondientes en la DB real".
Base.metadata.create_all(bind=motor)

print("--- BASE DE DATOS CREADA ---")

# 6. USAR LA BASE DE DATOS (Sesión)
Session = sessionmaker(bind=motor)
db = Session() # Es como el 'cursor', pero más inteligente

# A. CREAR (INSERT)
print("\n--- GUARDANDO DATOS ---")
nuevo_usuario = Usuario(nombre="Ana", edad=25) # Creamos el objeto
db.add(nuevo_usuario) # Lo marcamos para guardar
db.commit() # Confirmamos (Igual que antes)

print(f"Usuario guardado con ID: {nuevo_usuario.id}")

# B. LEER (SELECT)
print("\n--- LEYENDO DATOS ---")
# Traducciòn: "Busca en la tabla Usuario, filtra por nombre 'Ana', dame el primero"
usuario_encontrado = db.query(Usuario).filter_by(nombre="Ana").first()

print(usuario_encontrado)