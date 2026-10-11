import sqlite3

def conectar():
    try:
        # Intentar conectarse a la base de datos
        conexion = sqlite3.connect("src/data/dataprod.db")
        cursor = conexion.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                categoria TEXT NOT NULL,
                precio REAL NOT NULL )
            """)
        return conexion, cursor
    except sqlite3.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None, None

conexion, cursor = conectar();


