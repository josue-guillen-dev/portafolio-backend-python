from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base, Session

app = FastAPI()

# CAMBIAR ESTO POR EL NOMBRE REAL DEL PROYECTO
DATABASE = "sqlite:///./nombre_db.db"

engine = create_engine(DATABASE, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- AQUI VAN TUS CLASES DE BASE DE DATOS (MODELOS) ---
# class Usuario(Base): ...

# CREAR LAS TABLAS
Base.metadata.create_all(bind=engine)