from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

# Importamos NUESTROS módulos
import models, schemas, auth
from database import engine, get_db

# 1. Crear las tablas automáticamente
# Esta línea le dice a SQL: "Mira el archivo models.py y crea todas esas tablas"
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def home():
    return {"mensaje": "E-commerce API Activa 🛒"}


""" #### Parte B: Ruta de Registro (POST /usuarios)
Aquí usamos el esquema `UsuarioCrear` para recibir datos y el modelo `Usuario` para guardar.
python """


# 2. Ruta de Registro
@app.post("/usuarios", response_model=schemas.UsuarioRespuesta)
# response_model dice: "Devuelve los datos usando el molde seguro (sin clave)"
def crear_usuario(usuario: schemas.UsuarioCrear, db: Session = Depends(get_db)):

    # Validar si el email ya existe
    # (Usamos el ORM para buscar)
    existe = (
        db.query(models.Usuario).filter(models.Usuario.email == usuario.email).first()
    )
    if existe:
        raise HTTPException(status_code=400, detail="Email ya registrado")

    # Encriptar clave usando nuestro modulo auth.py
    hash_clave = auth.obtener_password_hash(usuario.password)

    # Crear el objeto de Base de Datos
    nuevo_usuario = models.Usuario(
        nombre=usuario.nombre,
        email=usuario.email,
        password=hash_clave,
        es_admin=False,  # Por defecto nadie es admin
    )

    # Guardar
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    return nuevo_usuario


# ... (Todo tu código anterior) ...


# 3. RUTA DE LOGIN (Aquí está la verificación)
@app.post("/login")
def login(datos: schemas.UsuarioLogin, db: Session = Depends(get_db)):

    # 1. Buscamos al usuario por email
    usuario = (
        db.query(models.Usuario).filter(models.Usuario.email == datos.email).first()
    )

    # 2. Si no existe -> Error
    if usuario is None:
        raise HTTPException(status_code=404, detail="Email no registrado")

    # 3. AQUI ESTÁ LA VERIFICACIÓN QUE BUSCABAS
    # Usamos auth.verificar_password para comparar lo que escribió (datos.password)
    # con lo que está en la base de datos (usuario.password)
    if not auth.verificar_password(datos.password, usuario.password):
        raise HTTPException(status_code=400, detail="Contraseña incorrecta")

    # 4. Si pasa el if, es bienvenido
    return {
        "mensaje": f"Bienvenido {usuario.nombre}, has iniciado sesión correctamente 🔓"
    }


# ... (Todo tu código de usuarios y login arriba) ...

# --- ZONA DE PRODUCTOS ---


# 4. Crear Producto (POST)
@app.post("/productos", response_model=schemas.ProductoRespuesta)
def crear_producto(producto: schemas.ProductoCrear, db: Session = Depends(get_db)):
    # Creamos el modelo de base de datos usando los datos del esquema
    nuevo_producto = models.Producto(
        nombre=producto.nombre, precio=producto.precio, stock=producto.stock
    )

    db.add(nuevo_producto)
    db.commit()
    db.refresh(nuevo_producto)

    return nuevo_producto


# 5. Listar Productos (GET)
# response_model=list[...] es para decir que devolveremos UNA LISTA de productos
@app.get("/productos", response_model=list[schemas.ProductoRespuesta])
def ver_productos(db: Session = Depends(get_db)):
    # Buscamos todos en la tabla
    productos = db.query(models.Producto).all()
    return productos


##E#PEDIDOS########################


# 6. CREAR PEDIDO (El Jefe Final)
@app.post("/usuarios/{user_id}/pedidos")
def crear_pedido(
    user_id: int, pedido: schemas.PedidoCrear, db: Session = Depends(get_db)
):

    # PASO A: Crear el "Carrito" (La cabecera del pedido)
    # Inicialmente el total es 0
    nuevo_pedido = models.Pedido(usuario_id=user_id, total=0)
    db.add(nuevo_pedido)
    db.commit()
    db.refresh(nuevo_pedido)  # Esto es vital para obtener el nuevo_pedido.id

    total_acumulado = 0

    # PASO B: Recorrer la lista de productos que compró
    for item in pedido.items:
        # item tiene: producto_id, cantidad

        # 1. Buscamos el producto real en la BD para saber su precio
        producto_db = (
            db.query(models.Producto)
            .filter(models.Producto.id == item.producto_id)
            .first()
        )

        if not producto_db:
            raise HTTPException(
                status_code=404, detail=f"Producto {item.producto_id} no existe"
            )

        # (Opcional: Aquí podrías validar si hay stock suficiente)

        # 2. Calculamos subtotal
        costo = producto_db.precio * item.cantidad
        total_acumulado += costo

        # 3. Creamos el Detalle (La fila en la tabla intermedia)
        nuevo_detalle = models.DetallePedido(
            pedido_id=nuevo_pedido.id,  # Usamos el ID que acabamos de crear
            producto_id=item.producto_id,
            cantidad=item.cantidad,
            precio_unitario=producto_db.precio,
        )
        db.add(nuevo_detalle)

        # 4. (Opcional) Restar stock
        producto_db.stock -= item.cantidad

    # PASO C: Actualizar el total final del pedido
    nuevo_pedido.total = total_acumulado
    db.commit()

    return {
        "mensaje": "Pedido creado exitosamente",
        "id_pedido": nuevo_pedido.id,
        "total": total_acumulado,
    }
