from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Nombre de la base de datos real
URL_DATABASE = "sqlite:///./tienda_virtual.db"

# 1. Crear el motor
# check_same_thread=False es necesario solo en SQLite
engine = create_engine(URL_DATABASE, connect_args={"check_same_thread": False})

# 2. Crear la fábrica de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. Crear la base para los modelos
Base = declarative_base()

# 4. Dependencia para obtener la DB en cada ruta (Yield)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()