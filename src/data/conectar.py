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

        conexion.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    apellido TEXT NOT NULL,
                    email TEXT NOT NULL,
                    contrasena TEXT NOT NULL,
                    rol TEXT NOT NULL  )
                """)

        usuario_admin = ("Admin", "Admin", "glrd4726@gmail.com", "Admin", "Admin")
        existe_admin = conexion.execute(
            "SELECT 1 FROM usuarios WHERE nombre = ? AND email = ? LIMIT 1",
            (usuario_admin[0], usuario_admin[2]),
        ).fetchone()
        if existe_admin is None:
            conexion.execute(
                "INSERT INTO usuarios (nombre, apellido, email, contrasena, rol) VALUES (?,?,?,?,?)",
                usuario_admin,
            )
        conexion.commit()
        
                
        return conexion
    except sqlite3.Error as e:
        input(f"Error al conectar a la base de datos: {e}")
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

def obtener_productos():
    """
    Función para obtener todos los productos de la base de datos.
    Parámetros:
    - Ninguno
    Retorna:
    - Lista de tuplas con los productos o None en caso de error
    """
    conexion = conectar()
    if conexion is not None:
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM productos")
            productos = cursor.fetchall()
            return productos
        except sqlite3.Error as e:
            print(f"Error al obtener los productos: {e}")
            return None
        finally:
            cerrar_conexion(conexion)
    else:
        print("No se pudo conectar a la base de datos.")
        return None
