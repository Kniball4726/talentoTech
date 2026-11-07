import os
import sqlite3
from pathlib import Path
import sys


def _ruta_base_datos() -> Path:
    if not getattr(sys, "frozen", False):
        return Path(__file__).resolve().with_name("inventario.db")
    if sys.platform == "win32":
        directorio = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
    elif sys.platform == "darwin":
        directorio = Path.home() / "Library" / "Application Support"
    else:
        directorio = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))
    return directorio / "TalentoTech" / "inventario.db"


DB_PATH = _ruta_base_datos()

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
        DB_PATH.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        conexion = sqlite3.connect(DB_PATH, timeout=5)
        if os.name != "nt":
            os.chmod(DB_PATH, 0o600)
        conexion.execute("PRAGMA foreign_keys = ON")
        
        conexion.execute("""
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                descripcion TEXT NOT NULL,
                cantidad INTEGER NOT NULL,
                precio REAL NOT NULL,
                categoria TEXT NOT NULL )
            """)

        conexion.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    apellido TEXT NOT NULL,
                    email TEXT NOT NULL,
                    contrasena TEXT NOT NULL,
                    rol TEXT NOT NULL  )
                """)

        conexion.execute("""
            CREATE TABLE IF NOT EXISTS intentos_login (
                nombre_usuario TEXT PRIMARY KEY,
                intentos INTEGER NOT NULL,
                bloqueado_hasta REAL NOT NULL
            )
            """)
        conexion.commit()
        return conexion
    except (sqlite3.Error, OSError):
        print("Error: no fue posible conectar con la base de datos.")
        if conexion is not None:
            conexion.close()
        return None

def cerrar_conexion(conexion):
    """
    Función para cerrar la conexión con la base de datos SQLite.
    Parámetros:
    - conexion: Objeto de conexión a la base de datos
    Retorna:
    - Ninguno
    """
    if conexion:
        conexion.close()