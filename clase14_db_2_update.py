import sqlite3

# 2. CONEXION (El Jefe)
# Si el archivo no existe, lo crea. Si existe, lo abre.
conexion = sqlite3.connect("mi_escuela.db")

# 3. CURSOR (El Asistente)
# Contratamos a quien va a mover los papeles.
cursor = conexion.cursor()

# --- FASE 1: PREPARAR EL TERRENO (Crear e Insertar) ---

# SOLUCION AL ERROR: Borramos la tabla vieja para que no moleste
# Esto asegura que la tabla se cree de nuevo con las 2 columnas correctas
cursor.execute("DROP TABLE IF EXISTS alumnos")

# 4. CREAR TABLA
# Le decimos al asistente: "Prepara una hoja nueva llamada 'alumnos' si no existe".
cursor.execute(
    """ 
        CREATE TABLE IF NOT EXISTS alumnos(
        nombre TEXT,
        edad INTEGER
        )
""")

# 5. INSERTAR DATOS INICIALES (Para tener a quien editar)
# Vamos a meter a 'Pepito' que tiene 10 años.
cursor.execute("INSERT INTO alumnos VALUES ('Pepito', 10)")
cursor.execute("INSERT INTO alumnos VALUES ('Juanita', 18)")

# Guardamos estos cambios iniciales
conexion.commit()
print("Datos iniciales creados: Pepito (10) y Juanita (12).")

# --- FASE 2: LA ACTUALIZACION (UPDATE) ---

print("\n--- AHORA VAMOS A ACTUALIZAR ---")
# Imagina que es el cumpleaños de Pepito. Cumple 11.

# Paso A: Definimos que queremos hacer
nueva_edad = 11
persona_a_actualizar = 'Pepito'

# Paso B: La Orden SQL (UPDATE)
# TRADUCCION: "Actualiza la tabla alumnos, pon la edad en 11, DONDE el nombre sea Pepito"

sql = "UPDATE alumnos SET edad = ? WHERE nombre = ?"

# Paso C: Ejecutamos la orden con los datos
cursor.execute(sql,(nueva_edad, persona_a_actualizar))

# Paso D: FIRMAR (Commit)
# Sin esto, el cambio de edad se pierde.
conexion.commit()

print("¡Actualización realizada!")

# --- FASE 3: VERIFICAR ---
print("\n--- RESULTADO FINAL EN LA BASE DE DATOS ---")

cursor.execute("SELECT * FROM alumnos")# Traeme todo
todos = cursor.fetchall()

for alumno in todos:
    print(alumno) # Deberias ver a Pepito con 11, no con 10.
    
# 6. CERRAR
conexion.close()