from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base, Session

app = FastAPI()

DATABASE= "sqlite:///./peliculas_db.db"

engine = create_engine(DATABASE, connect_args= {"check_same_thread": False})

SessionLocal = sessionmaker(autocommit= False, autoflush=False, bind=engine)

base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class PeliculasDB(base):
    __tablename__ = "peliculas"
    
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, index=True)
    director = Column(String)
    vista = Column(Boolean, default=False)
    
base.metadata.create_all(bind= engine)

class PeliculaNueva(BaseModel):
    titulo: str
    director: str

@app.post("/peliculas")
def pelicula_nueva(pelicula: PeliculaNueva, db: Session = Depends(get_db)):
    nueva = PeliculasDB(
        titulo = pelicula.titulo,
        director = pelicula.director
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    
    return nueva

@app.get("/peliculas")
def ver_pelicula(db: Session = Depends(get_db)):
    ver = db.query(PeliculasDB).all()
    return ver

@app.put("/peliculas/{id}/vista")
def actualizar(id_pelicula: int , db: Session = Depends(get_db)):
    buscar = db.query(PeliculasDB).filter(PeliculasDB.id == id_pelicula).first()
    
    if buscar is None:
        raise HTTPException(status_code=404, detail="pelicula no existe")
    
    buscar.vista = not buscar.vista
    
    db.commit()
    return {"mensaje":"pelicula vista"}

