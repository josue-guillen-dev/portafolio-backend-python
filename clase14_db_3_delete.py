import sqlite3

print("--- SISTEMA DE EXPULSION ---")

conexion = sqlite3.connect("mi_escuela.db")
cursor = conexion.cursor()

# 1. MOSTRAMOS LA LISTA ACTUAL
print("Alumnos Matriculados: ")
cursor.execute("SELECT * FROM alumnos")
lista = cursor.fetchall()
for alumno in lista:
    print(alumno)
    
# 2. PREGUNTAMOS A QU(IEN BORRAR
nombre_borrar = input("\n A quien desea eliminar de la base de datos: ")

# 3. LA ORDEN DE BORRADO
# TRADUCCION: "Borra de la tabla alumnos DONDE el nombre sea igual a..."
sql = "DELETE FROM alumnos WHERE nombre = ?"
cursor.execute(sql,(nombre_borrar, ))

# 4. FIRMAR (Commit)
conexion.commit()

# 5. VALIDAMOS SI BORRO ALGO
if cursor.rowcount > 0:
    print(f"Adios {nombre_borrar} a sido eliminado")
else:
    print("No encontre a nadie con ese nombre")
    
# 6. MOSTRAMOS COMO QUEDO LA TABLA
print("\n--- LISTA FINAL ---")
cursor.execute("SELECT * FROM alumnos")
for alumno in cursor.fetchall():
    print(alumno)

conexion.close()