from getpass import getpass
import sqlite3

from colorama import Style, Fore, init

from src.logic.autenticacion import hash_password
from src.logic.productos import limpiar_pantalla
import src.data.conectar as db


_LONGITUD_MINIMA = 12

init(autoreset=True)


def _es_admin(rol: str) -> bool:
    if rol == "Admin":
        return True
    print(Fore.RED + Style.BRIGHT + "\nAcceso denegado. Se requiere el rol Admin.")
    input("\nPresione Enter para continuar...")
    return False


def _solicitar_contrasena() -> str | None:
    password = getpass("Ingrese una contraseña (mínimo 12 caracteres): ")
    confirmacion = getpass("Confirme la contraseña: ")
    if password != confirmacion:
        print(Fore.RED + Style.BRIGHT + "\nLas contraseñas no coinciden.")
        return None
    if not _LONGITUD_MINIMA <= len(password) <= 1024:
        print(
            Fore.RED
            + Style.BRIGHT
            + "\nLa contraseña debe tener entre 12 y 1024 caracteres."
        )
        return None
    return password


def agregar_usuario(rol: str):
    if not _es_admin(rol):
        return
    limpiar_pantalla()
    print(Fore.YELLOW + Style.BRIGHT + "=================================================")
    print(Fore.GREEN + Style.BRIGHT + "Agregar nuevo usuario")
    print(Fore.YELLOW + Style.BRIGHT + "=================================================")
    nombre_usuario = input("\nIngrese el nombre de usuario: ").strip()
    apellido = input("Ingrese el apellido: ").strip()
    email = input("Ingrese el correo electrónico: ").strip()
    contrasena = _solicitar_contrasena()
    nuevo_rol = input("Ingrese el rol (Admin/Usuario): ").strip().capitalize()

    if not nombre_usuario or not apellido or not email or contrasena is None:
        print(Fore.RED + Style.BRIGHT + "\nError: Todos los campos son obligatorios.")
        input("\nPresione Enter para continuar...")
        return
    if nuevo_rol not in ("Admin", "Usuario"):
        print(Fore.RED + Style.BRIGHT + "\nError: Rol inválido.")
        input("\nPresione Enter para continuar...")
        return

    conexion = db.conectar()
    if conexion is None:
        print(Fore.RED + Style.BRIGHT + "\nError al conectar a la base de datos.")
        input("\nPresione Enter para continuar...")
        return

    try:
        existe = conexion.execute(
            "SELECT 1 FROM usuarios WHERE nombre = ? COLLATE NOCASE LIMIT 1",
            (nombre_usuario,),
        ).fetchone()
        if existe:
            print(Fore.RED + Style.BRIGHT + "\nEse nombre de usuario ya está registrado.")
        else:
            conexion.execute(
                "INSERT INTO usuarios (nombre, apellido, email, contrasena, rol) "
                "VALUES (?, ?, ?, ?, ?)",
                (
                    nombre_usuario,
                    apellido,
                    email,
                    hash_password(contrasena),
                    nuevo_rol,
                ),
            )
            conexion.commit()
            print(Fore.GREEN + Style.BRIGHT + "\nUsuario agregado correctamente.")
    except sqlite3.Error:
        conexion.rollback()
        print(Fore.RED + Style.BRIGHT + "\nError de base de datos al agregar usuario.")
    finally:
        conexion.close()

    input("\nPresione Enter para continuar...")


def mostrar_usuarios(rol: str):
    if not _es_admin(rol):
        return
    limpiar_pantalla()
    print(Fore.YELLOW + Style.BRIGHT + "=================================================")
    print(Fore.GREEN + Style.BRIGHT + "Lista de usuarios")
    print(Fore.YELLOW + Style.BRIGHT + "=================================================")

    conexion = db.conectar()
    if conexion is not None:
        try:
            usuarios = conexion.execute(
                "SELECT id, nombre, rol FROM usuarios ORDER BY id"
            ).fetchall()
            if usuarios:
                for usuario in usuarios:
                    print(
                        f"ID: {usuario[0]}\nNombre de usuario: {usuario[1]}\n"
                        f"Rol: {usuario[2]}\n========================="
                    )
            else:
                print(Fore.RED + Style.BRIGHT + "\nNo hay usuarios registrados.")
        except sqlite3.Error:
            print(Fore.RED + Style.BRIGHT + "\nError al consultar los usuarios.")
        finally:
            conexion.close()
    else:
        print(Fore.RED + Style.BRIGHT + "\nError al conectar a la base de datos.")

    input("\nPresione Enter para continuar...")


def modificar_usuario(rol: str):
    if not _es_admin(rol):
        return
    limpiar_pantalla()
    print(Fore.YELLOW + Style.BRIGHT + "=================================================")
    print(Fore.GREEN + Style.BRIGHT + "Modificar usuario")
    print(Fore.YELLOW + Style.BRIGHT + "=================================================")

    conexion = db.conectar()
    if conexion is None:
        print(Fore.RED + Style.BRIGHT + "\nError al conectar a la base de datos.")
        input("\nPresione Enter para continuar...")
        return

    try:
        usuarios = conexion.execute(
            "SELECT id, nombre, rol FROM usuarios ORDER BY id"
        ).fetchall()
        for usuario in usuarios:
            print(f"ID: {usuario[0]} | Usuario: {usuario[1]} | Rol: {usuario[2]}")
        usuario_id = int(input("\nIngrese el ID del usuario a modificar: "))
        usuario = conexion.execute(
            "SELECT id, nombre, rol FROM usuarios WHERE id = ?", (usuario_id,)
        ).fetchone()
        if usuario is None:
            print(Fore.RED + Style.BRIGHT + "\nNo se encontró ese usuario.")
            return

        nuevo_nombre = input(
            f"Nuevo nombre de usuario (actual: {usuario[1]}): "
        ).strip() or usuario[1]
        rol_ingresado = input(
            f"Nuevo rol (actual: {usuario[2]}): "
        ).strip()
        nuevo_rol = rol_ingresado.capitalize() if rol_ingresado else usuario[2]
        if nuevo_rol not in ("Admin", "Usuario"):
            print(Fore.RED + Style.BRIGHT + "\nError: Rol inválido.")
            return

        duplicado = conexion.execute(
            "SELECT 1 FROM usuarios WHERE nombre = ? COLLATE NOCASE AND id != ?",
            (nuevo_nombre, usuario_id),
        ).fetchone()
        if duplicado:
            print(Fore.RED + Style.BRIGHT + "\nEse nombre de usuario ya está registrado.")
            return
        if usuario[2] == "Admin" and nuevo_rol != "Admin":
            admins = conexion.execute(
                "SELECT COUNT(*) FROM usuarios WHERE rol = 'Admin'"
            ).fetchone()[0]
            if admins <= 1:
                print(Fore.RED + Style.BRIGHT + "\nNo se puede quitar el último administrador.")
                return

        conexion.execute(
            "UPDATE usuarios SET nombre = ?, rol = ? WHERE id = ?",
            (nuevo_nombre, nuevo_rol, usuario_id),
        )
        conexion.commit()
        print(Fore.GREEN + Style.BRIGHT + "\nUsuario modificado correctamente.")
    except ValueError:
        print(Fore.RED + Style.BRIGHT + "\nIngrese un ID válido.")
    except sqlite3.Error:
        conexion.rollback()
        print(Fore.RED + Style.BRIGHT + "\nError al modificar el usuario.")
    finally:
        conexion.close()
    input("\nPresione Enter para continuar...")


def eliminar_usuario(rol: str):
    if not _es_admin(rol):
        return
    limpiar_pantalla()
    print(Fore.YELLOW + Style.BRIGHT + "=================================================")
    print(Fore.GREEN + Style.BRIGHT + "Eliminar usuario")
    print(Fore.YELLOW + Style.BRIGHT + "=================================================")

    conexion = db.conectar()
    if conexion is None:
        print(Fore.RED + Style.BRIGHT + "\nError al conectar a la base de datos.")
        input("\nPresione Enter para continuar...")
        return

    try:
        usuarios = conexion.execute(
            "SELECT id, nombre, rol FROM usuarios ORDER BY id"
        ).fetchall()
        for usuario in usuarios:
            print(f"ID: {usuario[0]} | Usuario: {usuario[1]} | Rol: {usuario[2]}")
        usuario_id = int(input("\nIngrese el ID del usuario a eliminar: "))
        usuario = conexion.execute(
            "SELECT id, rol FROM usuarios WHERE id = ?", (usuario_id,)
        ).fetchone()
        if usuario is None:
            print(Fore.RED + Style.BRIGHT + "\nNo se encontró ese usuario.")
            return
        if usuario[1] == "Admin":
            admins = conexion.execute(
                "SELECT COUNT(*) FROM usuarios WHERE rol = 'Admin'"
            ).fetchone()[0]
            if admins <= 1:
                print(Fore.RED + Style.BRIGHT + "\nNo se puede eliminar el último administrador.")
                return

        conexion.execute("DELETE FROM usuarios WHERE id = ?", (usuario_id,))
        conexion.commit()
        print(Fore.GREEN + Style.BRIGHT + "\nUsuario eliminado correctamente.")
    except ValueError:
        print(Fore.RED + Style.BRIGHT + "\nIngrese un ID válido.")
    except sqlite3.Error:
        conexion.rollback()
        print(Fore.RED + Style.BRIGHT + "\nError al eliminar el usuario.")
    finally:
        conexion.close()
    input("\nPresione Enter para continuar...")
