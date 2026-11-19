import sqlite3
import os

# Ruta del archivo de base de datos
RUTA_DB = os.path.join(
    os.path.dirname(__file__),
    "formulario.db" #nombre de la bd
)

print("Base de datos utilizada:", RUTA_DB)

# Crear la tabla usuarios
def crear_tabla():
    conexion = sqlite3.connect(RUTA_DB)

    conexion.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            telefono TEXT NOT NULL,
            correo TEXT NOT NULL,
            genero TEXT NOT NULL,
            colores TEXT NOT NULL,
            ocupacion TEXT NOT NULL,
            imagen TEXT
        )
    """)

    conexion.commit()
    conexion.close()


# Guardar los datos del formulario
def guardar_usuario(nombre, telefono, correo,genero, colores, ocupacion, imagen):
    conexion = sqlite3.connect(RUTA_DB)

    conexion.execute("""
        INSERT INTO usuarios (nombre, telefono, correo, genero, colores, ocupacion, imagen)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (nombre, telefono, correo, genero, colores, ocupacion, imagen),)

    conexion.commit()
    conexion.close()

# Mostrar los datos almacenados
def mostrar_usuario():
    conexion = sqlite3.connect(RUTA_DB)
    conexion.row_factory=sqlite3.Row
    cursor=conexion.cursor()

    cursor.execute("SELECT *FROM usuarios")
    usuarios=cursor.fetchall()

    conexion.close()
    return (usuarios)


# Buscar un usuario por su ID
def buscar_usuario(id_usuario):
    conexion = sqlite3.connect(RUTA_DB)
    conexion.row_factory=sqlite3.Row
    cursor=conexion.cursor()
    
    cursor.execute("SELECT *FROM usuarios WHERE id=?", (id_usuario,))
    usuario=cursor.fetchone()
    conexion.close()
    return (usuario)

# Editar usuario
def editar_usuario(id_usuario, nombre, telefono, correo, genero, colores, ocupacion, imagen):
    conexion = sqlite3.connect(RUTA_DB)
    cursor=conexion.cursor()

    cursor.execute("""
        UPDATE usuarios SET nombre=?, telefono=?, correo=?, genero=?, colores=?, ocupacion=?, imagen=? where id=?
    """,
        (
            nombre, telefono, correo, genero, colores, ocupacion, imagen, id_usuario,
        ),
    )

    conexion.commit()
    conexion.close()


#eliminar imagen
def eliminar_imagen(id_usuario, CARPETA_IMAGENES):
    conexion = sqlite3.connect(RUTA_DB)
    conexion.row_factory=sqlite3.Row
    cursor=conexion.cursor()

    cursor.execute("SELECT imagen FROM usuarios WHERE id=?", (id_usuario,))
    usuario=cursor.fetchone()

    if usuario and usuario['imagen']:
        nombre_imagen=usuario['imagen']
        ruta_completa=os.path.join(CARPETA_IMAGENES, nombre_imagen)

        if os.path.exists(ruta_completa):
            os.remove(ruta_completa)

    conexion.close()
    return (usuario)


def eliminar_usuario(id_usuario, CARPETA_IMAGENES):
    conexion = sqlite3.connect(RUTA_DB)
    cursor=conexion.cursor()
    eliminar_imagen(id_usuario, CARPETA_IMAGENES)

    cursor.execute(" DELETE FROM usuarios where id=?", (id_usuario,))
    conexion.commit()
    conexion.close()  


