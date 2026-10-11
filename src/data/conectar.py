import sqlite3


def conectar():
    """
    Función para establecer una conexión con la base de datos SQLite.
    Si la conexión es exitosa, se crea la tabla "productos" si no existe.
    Parámetros:
    - Ninguno
    Retorna:
    - Objeto de conexión a la base de datos o None en caso de error
    """
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
    """
    Función para cerrar la conexión a la base de datos SQLite.
    Parámetros:
    - conexion: Objeto de conexión a la base de datos
    Retorna:
    - Ninguno
    """
    if conexion is not None:
        conexion.close()
