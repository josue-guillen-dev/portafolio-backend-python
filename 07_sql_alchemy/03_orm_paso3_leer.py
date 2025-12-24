from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. Configuración (Siempre igual)
motor = create_engine("sqlite:///mi_primera_orm.db", echo=False) # echo=False para que no moleste el texto tecnico
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

print("--- BUSCANDO DATOS ---")

# A. TRAER TODOS (fetchall)
# Traducción: "Consulta la tabla Persona y dame todo (.all)"
todos = db.query(Persona).all()

print(f"Encontré {len(todos)} personas:")
for p in todos:
    print(f"- {p}") # Imprime bonito gracias a __repr__

# B. FILTRAR (WHERE)
# Traducción: "Consulta Persona, filtra donde nombre sea 'Juan', dame el primero"
juan = db.query(Persona).filter(Persona.nombre == "Juan").first()

if juan:
    print(f"\n¡Encontré a Juan! Su ID es {juan.id}")
else:
    print("\nJuan no está en la base de datos.")

db.close()