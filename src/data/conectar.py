import sqlite3

def conectar():
    conexion = None
    try:
        # Intentar conectarse a la base de datos
        conexion = sqlite3.connect("src/data/dataprod.db")
        conexion.execute("""
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                categoria TEXT NOT NULL,
                precio REAL NOT NULL )
            """)
        return conexion
    except sqlite3.Error as e:
        if conexion is not None:
            conexion.close()
        print(f"Error al conectar a la base de datos: {e}")
        return None


def cerrar_conexion(conexion):
    if conexion is not None:
        conexion.close()
