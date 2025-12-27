from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from database import get_db, Base

# 1. CONFIGURACION DE BASE DE DATOS DE PRUEBA
# Usamos una DB en memoria (se borra al terminar el test)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --- CORRECCION 1: LIMPIEZA ---
# Borramos las tablas viejas antes de crear las nuevas
# Así evitamos el error de "Usuario ya existe

# Creamos las tablas en la DB de prueba
Base.metadata.create_all(bind=engine)


# 2. TRUCO DE MAGIA (Dependency Override)
# Le decimos a FastAPI: "Cuando alguien pida get_db, NO uses la real, usa la de prueba"
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

# 3. EL CLIENTE (Tu navegador falso)
client = TestClient(app)

# --- AQUI EMPIEZAN LAS PRUEBAS ---


def test_registro_usuario():
    # Simulamos enviar datos al registro
    datos = {"nombre": "Tester", "email": "test@mail.com", "password": "123"}

    response = client.post("/usuarios", json=datos)

    # Verificaciones (Asserts)
    assert response.status_code == 200  # Que no de error
    data = response.json()
    assert data["email"] == "test@mail.com"  # Que devuelva el email correcto
    assert "password" not in data  # Que NO devuelva la clave (seguridad)


def test_login_exitoso():
    # Usamos los mismos datos para entrar (ya se creó arriba)
    datos_login = {"email": "test@mail.com", "password": "123"}

    response = client.post("/login", json=datos_login)

    assert response.status_code == 200
    assert "Bienvenido" in response.json()["mensaje"]


def test_login_fallido():
    # Intentamos con clave mala
    datos_malos = {"email": "test@mail.com", "password": "000"}

    response = client.post("/login", json=datos_malos)

    assert response.status_code == 400  # Debe fallar

def test_producto():
    datos_productos= {
        "nombre": "lapto gamer",
        "precio": 150000,
        "stock": 12
    }
    response = client.post("/productos", json=datos_productos)
    assert response.status_code == 200
    
    respuesta = response.json()
    assert respuesta["nombre"] == "lapto gamer"
    assert respuesta["precio"] == 150000
    assert "id" in respuesta