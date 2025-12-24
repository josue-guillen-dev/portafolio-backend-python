from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. Configuración (Igual siempre)
motor = create_engine("sqlite:///mi_primera_orm.db", echo=False)
Base = declarative_base()


class Persona(Base):
    __tablename__ = "personas"
    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    edad = Column(Integer)

    def __repr__(self):
        return f"Persona: {self.nombre} ({self.edad})"


Session = sessionmaker(bind=motor)
db = Session()

print("--- ACTUALIZANDO DATOS ---")

# A. UPDATE (Actualizar)
# Paso 1: Buscar a quien queremos cambiar
# Buscamos a "Juan" (el primero que encuentre)

# MALA PRACTICA (Peligroso si hay homónimos)
# juan = db.query(Persona).filter(Persona.nombre == "Juan").first()

# BUENA PRACTICA (Seguro)
# Buscamos exactamente al usuario con ID 1
juan_seguro = db.query(Persona).filter(Persona.id == 1).first()

if juan_seguro:
    juan_seguro.edad = 30
    db.commit()
    print(f"Se actualizó a: {juan_seguro}")
else:
    print("No existe nadie con el ID 1")

print("\n--- BORRANDO DATOS ---")

# B. DELETE (Borrar)
# Paso 1: Buscar a la victima
# Buscamos a "Ana"
ana = db.query(Persona).filter(Persona.nombre == "Ana").first()

if ana:
    # Paso 2: Marcarla para borrar
    db.delete(ana)

    # Paso 3: Confirmar
    db.commit()
    print("Ana ha sido eliminada de la base de datos.")
else:
    print("Ana ya no existe.")

db.close()
