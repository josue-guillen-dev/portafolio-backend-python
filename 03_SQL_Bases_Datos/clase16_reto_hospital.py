import sqlite3


def inicializar_db():
    conexion = sqlite3.connect("hospital.db")
    cursor = conexion.cursor()
    cursor.execute(
        """ CREATE TABLE IF NOT EXISTS pacientes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        edad INTEGER,
        enfermedad TEXT
        ) 
        """
    )
    conexion.commit()
    conexion.close()


class Paciente:
    def __init__(self, nombre, edad, enfermedad):
        self.nombre = nombre
        self.edad = edad
        self.enfermedad = enfermedad

    def presentarse(self):
        print(f"Soy {self.nombre}, tengo {self.edad} años y sufro de {self.enfermedad}")

    def guardar(self):
        conexion = sqlite3.connect("hospital.db")
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO pacientes (nombre,edad,enfermedad) VALUES (?,?,?)",
            (self.nombre, self.edad, self.enfermedad),
        )
        conexion.commit()
        conexion.close()
        print("Paciente Guardado en el Sistema")


def ver_paciente():
    conexion = sqlite3.connect("hospital.db")
    cursor = conexion.cursor()
    lista = cursor.execute("SELECT * FROM pacientes")
    for paciente in lista:
        print(paciente)

    conexion.close()


inicializar_db()

nuevo_paciente = Paciente("josue", 31, "dolor pulmonar")
nuevo_paciente.presentarse()
nuevo_paciente.guardar()
ver_paciente()
