from src.logic.productos import limpiar_pantalla
from colorama import Style, Fore, Back, init
import sqlite3
import src.data.conectar as db


init(autoreset=True)


def agregar_usuario():
    limpiar_pantalla()
    print(Fore.YELLOW+Style.BRIGHT+"=================================================")
    print(Fore.GREEN+Style.BRIGHT+"Agregar nuevo usuario")
    print(Fore.YELLOW+Style.BRIGHT+"=================================================")
    nombre_usuario: str = input("\nIngrese el nombre de usuario: ").strip().capitalize()
    apellido: str = input("Ingrese el apellido: ").strip().capitalize()
    email: str = input("Ingrese el correo electrónico: ").strip()
    contrasena: str = input("Ingrese la contraseña: ").strip()
    rol: str = input("Ingrese el rol (Admin/Usuario): ").strip().capitalize()

    if not nombre_usuario or not apellido or not email or not contrasena:
        print(Fore.RED+Style.BRIGHT+"\nError: Todos los campos son obligatorios.")
        input("\nPresione Enter para continuar...")
        return

    if rol not in ["Admin", "Usuario"]:
        print(Fore.RED+Style.BRIGHT+"\nError: Rol inválido. Debe ser 'Admin' o 'Usuario'.")
        input("\nPresione Enter para continuar...")
        return

    conexion = db.conectar()
    if conexion is None:
        print(Fore.RED+Style.BRIGHT+"\nError al conectar a la base de datos.")
        input("\nPresione Enter para continuar...")
        return

    try:
        conexion.execute(
            "INSERT INTO usuarios (nombre, apellido, email, contrasena, rol) "
            "VALUES (?, ?, ?, ?, ?)",
            (nombre_usuario, apellido, email, contrasena, rol),
        )
        conexion.commit()
        print(Fore.GREEN+Style.BRIGHT+f"\nUsuario '{nombre_usuario}' agregado correctamente.")
    except sqlite3.IntegrityError as e:
        conexion.rollback()
        print(Fore.RED+Style.BRIGHT+f"\nError de integridad al agregar usuario: {e}")
    except sqlite3.Error as e:
        conexion.rollback()
        print(Fore.RED+Style.BRIGHT+f"\nError de base de datos al agregar usuario: {e}")
    finally:
        conexion.close()

    input("\nPresione Enter para continuar...")

def mostrar_usuarios():
    limpiar_pantalla()
    print(Fore.YELLOW+Style.BRIGHT+"=================================================")
    print(Fore.GREEN+Style.BRIGHT+"Lista de usuarios")
    print(Fore.YELLOW+Style.BRIGHT+"=================================================")

    conexion = db.conectar()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT id, nombre, rol FROM usuarios")
            usuarios = cursor.fetchall()

            if usuarios:
                for usuario in usuarios:
                    print(f"ID: {usuario[0]}\nNombre de usuario: {usuario[1]}\nRol: {usuario[2]}\n=========================")
            else:
                print(Fore.RED+Style.BRIGHT+"\nNo hay usuarios registrados.")
        except Exception as e:
            print(Fore.RED+Style.BRIGHT+f"\nError inesperado al mostrar usuarios: {e}")
        finally:
            conexion.close()
    else:
        print(Fore.RED+Style.BRIGHT+"\nError al conectar a la base de datos.")

    input("\nPresione Enter para continuar...")

def modificar_usuario():
    limpiar_pantalla()
    print(Fore.YELLOW+Style.BRIGHT+"=================================================")
    print(Fore.GREEN+Style.BRIGHT+"Modificar usuario")
    print(Fore.YELLOW+Style.BRIGHT+"=================================================")
    mostrar_usuarios()
    usuario_id: int = int(input("\nIngrese el ID del usuario a modificar: "))

    conexion = db.conectar()
    if conexion:
        
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT id, nombre, rol FROM usuarios WHERE id = ?", (usuario_id,))
            usuario = cursor.fetchone()

            if usuario:
                nuevo_nombre: str = input(f"Ingrese el nuevo nombre de usuario (actual: {usuario[1]}): ").strip().capitalize()
                nuevo_rol: str = input(f"Ingrese el nuevo rol (actual: {usuario[2]}): ").strip().capitalize()

                if nuevo_rol not in ["Admin", "Usuario"]:
                    print(Fore.RED+Style.BRIGHT+"\nError: Rol inválido. Debe ser 'Admin' o 'Usuario'.")
                    input("\nPresione Enter para continuar...")
                    return

                cursor.execute(
                    "UPDATE usuarios SET nombre = ?, rol = ? WHERE id = ?",
                    (nuevo_nombre, nuevo_rol, usuario_id),
                )
                conexion.commit()
                print(Fore.GREEN+Style.BRIGHT+f"\nUsuario modificado correctamente.")
            else:
                print(Fore.RED+Style.BRIGHT+"\nNo se encontró un usuario con ese ID.")
        except Exception as e:
            print(Fore.RED+Style.BRIGHT+f"\nError inesperado al modificar usuario: {e}")
        finally:
            conexion.close()
    else:
        print(Fore.RED+Style.BRIGHT+"\nError al conectar a la base de datos.")

    input("\nPresione Enter para continuar...")

def eliminar_usuario():
    limpiar_pantalla()
    print(Fore.YELLOW+Style.BRIGHT+"=================================================")
    print(Fore.GREEN+Style.BRIGHT+"Eliminar usuario")
    print(Fore.YELLOW+Style.BRIGHT+"=================================================")
    mostrar_usuarios()
    usuario_id: int = int(input("\nIngrese el ID del usuario a eliminar: "))

    conexion = db.conectar()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT id FROM usuarios WHERE id = ?", (usuario_id,))
            usuario = cursor.fetchone()

            if usuario:
                cursor.execute("DELETE FROM usuarios WHERE id = ?", (usuario_id,))
                conexion.commit()
                print(Fore.GREEN+Style.BRIGHT+f"\nUsuario eliminado correctamente.")
            else:
                print(Fore.RED+Style.BRIGHT+"\nNo se encontró un usuario con ese ID.")
        except Exception as e:
            print(Fore.RED+Style.BRIGHT+f"\nError inesperado al eliminar usuario: {e}")
        finally:
            conexion.close()
    else:
        print(Fore.RED+Style.BRIGHT+"\nError al conectar a la base de datos.")

    input("\nPresione Enter para continuar...")
