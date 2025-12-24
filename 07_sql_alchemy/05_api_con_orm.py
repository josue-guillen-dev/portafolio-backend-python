# --- 1. IMPORTACIONES ---
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base, Session

# --- 2. CONFIGURACIÓN BASE DE DATOS (El Motor) ---
# Creamos el archivo 'tareas_pro.db'
SQLALCHEMY_DATABASE_URL = "sqlite:///./tareas_pro.db"

# connect_args es necesario solo para SQLite
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# La fábrica de sesiones (Juanito el asistente)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# El molde base para las tablas
Base = declarative_base()

# --- 3. MODELO DE BASE DE DATOS (La Tabla) ---
class TareaDB(Base):
    __tablename__ = "tareas"
    
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, index=True)
    descripcion = Column(String)
    completada = Column(Boolean, default=False) # ¡SQLAlchemy maneja Booleanos!

# Creamos las tablas en el archivo
Base.metadata.create_all(bind=engine)

# --- 4. ESQUEMAS DE PYDANTIC (Validación de Datos) ---
# Esto es lo que el usuario nos envía
class TareaNueva(BaseModel):
    titulo: str
    descripcion: str
    completada: bool = False

# --- 5. DEPENDENCIA (El Truco Profesional) ---
# Esta funcion entrega la base de datos a quien la pida y la cierra al terminar.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- 6. LA API (Rutas) ---
app = FastAPI()

@app.post("/tareas")
def crear_tarea(tarea: TareaNueva, db: Session = Depends(get_db)):
    # TRADUCCION ORM: "Crea un objeto TareaDB con los datos recibidos"
    nueva_tarea = TareaDB(
        titulo=tarea.titulo, 
        descripcion=tarea.descripcion, 
        completada=tarea.completada
    )
    
    db.add(nueva_tarea)  # "Juanito, anota esto"
    db.commit()          # "Firma y guarda"
    db.refresh(nueva_tarea) # "Dime qué ID le tocó"
    
    return nueva_tarea

@app.get("/tareas")
def leer_tareas(db: Session = Depends(get_db)):
    # TRADUCCION ORM: "SELECT * FROM tareas"
    return db.query(TareaDB).all()

@app.put("/tareas/{id_tarea}")
def actualizar_tarea(id_tarea: int, db: Session = Depends(get_db)):
    # 1. Buscar
    tarea_existente = db.query(TareaDB).filter(TareaDB.id == id_tarea).first()
    
    if tarea_existente is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    
    # 2. Modificar (Invertir estado: Si es True pasa a False y viceversa)
    tarea_existente.completada = not tarea_existente.completada
    
    # 3. Guardar
    db.commit()
    
    return {"mensaje": "Estado actualizado", "estado_actual": tarea_existente.completada}

@app.delete("/tareas/{id_tarea}")
def borrar_tarea(id_tarea: int, db: Session = Depends(get_db)):
    tarea = db.query(TareaDB).filter(TareaDB.id == id_tarea).first()
    
    if tarea is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
        
    db.delete(tarea) # "Bórralo"
    db.commit()      # "Confirma"
    
    return {"mensaje": "Tarea eliminada"}