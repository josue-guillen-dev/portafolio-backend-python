from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. Configuración (Igual que antes)
motor = create_engine("sqlite:///mi_primera_orm.db", echo=True)
Base = declarative_base()

# 2. Definimos la Clase (Tiene que ser IGUAL a la anterior)
class Persona(Base):
    __tablename__ = "personas"
    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    edad = Column(Integer)
    
    def __repr__(self):
        return f"Persona({self.nombre}, {self.edad} años)"
    
# --- ¡ESTO FALTABA! ---
# 2.5. Ordenamos crear las tablas si no existen
Base.metadata.create_all(bind=motor)
# ----------------------

# 3. Creamos la Sesión (Contratamos a Beto)
Session = sessionmaker(bind=motor)
db = Session()

print("--- GUARDANDO DATOS CON ORM ---")

# 4. Creamos Objetos (Puro Python, nada de SQL)
juan = Persona(nombre="Juan", edad=25)
ana = Persona(nombre="Ana", edad=30)

# 5. Le damos los objetos a la sesión
# "Beto, anota a estos dos"
db.add(juan)
db.add(ana)

# 6. Confirmamos (El Sello Oficial)
# Aquí es donde Beto traduce todo a SQL y lo envía
db.commit()

print(f"Guardados: {juan} y {ana}")
print(f"ID de Juan: {juan.id}") # ¡El ID se genera solo y se actualiza en el objeto!

db.close()