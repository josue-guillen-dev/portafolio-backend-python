from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
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
class UsuarioDB(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    email = Column(String, unique=True)


class PostDB(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String)
    cuerpo = Column(String)
    owner_id = Column(Integer, ForeignKey("usuarios.id"))


Base.metadata.create_all(bind=engine)


class UsuarioCrear(BaseModel):
    nombre: str
    email: str


class PostCrear(BaseModel):
    titulo: str
    cuerpo: str


@app.post("/usuarios")
def crear_usuario(usuario: UsuarioCrear, db: Session = Depends(get_db)):
    usuario_nuevo = UsuarioDB(nombre=usuario.nombre, email=usuario.email)
    db.add(usuario_nuevo)
    db.commit()
    db.refresh(usuario_nuevo)

    return usuario_nuevo


@app.post("/usuarios/{user_id}/posts")
def post(user_id: int, post: PostCrear, db: Session = Depends(get_db)):
    usuario = db.query(UsuarioDB).filter(UsuarioDB.id == user_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="usuario no existe")

    post_nuevo = PostDB(titulo=post.titulo, cuerpo=post.cuerpo, owner_id=user_id)
    db.add(post_nuevo)
    db.commit()
    db.refresh(post_nuevo)
    return post_nuevo


@app.get("/usuarios/{user_id}")
def ver_usuario(user_id: int, db: Session = Depends(get_db)):
    usuario = db.query(UsuarioDB).filter(UsuarioDB.id == user_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="usuario no existe")

    post = db.query(PostDB).filter(PostDB.owner_id == user_id).all()
    return {"id": usuario.id, "nombre": usuario.nombre, "Post": post}
