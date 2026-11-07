from getpass import getpass
import sqlite3

from colorama import Fore, Style, init

from src.logic.autenticacion import (
    autenticar,
    crear_administrador_inicial,
    hay_administrador_legacy,
    hay_usuarios,
    reemplazar_contrasena_admin_legacy,
)
from src.logic.productos import limpiar_pantalla
from src.gui.principal import menu


_LONGITUD_MINIMA = 12

init(autoreset=True)


def _solicitar_contrasena() -> str:
    while True:
        password = getpass("Nueva contraseña (mínimo 12 caracteres): ")
        confirmacion = getpass("Confirme la contraseña: ")
        if password != confirmacion:
            print(Fore.RED + "Las contraseñas no coinciden.")
        elif len(password) < _LONGITUD_MINIMA:
            print(Fore.RED + "La contraseña debe tener al menos 12 caracteres.")
        elif len(password) > 1024:
            print(Fore.RED + "La contraseña no puede superar 1024 caracteres.")
        else:
            return password


def _configurar_cuentas():
    if not hay_usuarios():
        print(
            Fore.YELLOW
            + Style.BRIGHT
            + "No hay usuarios. Configure la cuenta administradora inicial."
        )
        nombre = input("Nombre de usuario: ").strip()
        apellido = input("Apellido: ").strip()
        email = input("Correo electrónico: ").strip()
        if not nombre or not apellido or not email:
            raise ValueError("Nombre, apellido y correo son obligatorios.")
        crear_administrador_inicial(
            nombre, apellido, email, _solicitar_contrasena()
        )
        print(Fore.GREEN + "Cuenta administradora configurada.")
    elif hay_administrador_legacy():
        print(
            Fore.YELLOW
            + Style.BRIGHT
            + "La cuenta inicial conocida debe cambiar su contraseña antes de continuar."
        )
        reemplazar_contrasena_admin_legacy(_solicitar_contrasena())
        print(Fore.GREEN + "Contraseña inicial reemplazada.")


def login():
    try:
        _configurar_cuentas()
        for intento in range(5):
            limpiar_pantalla()
            print(Fore.YELLOW + Style.BRIGHT + "=====================================================")
            print(Fore.GREEN + Style.BRIGHT + "Hola, bienvenido al sistema de gestión de productos")
            print(Fore.YELLOW + Style.BRIGHT + "=====================================================")
            nombre_usuario = input("\nUsuario: ").strip()
            contrasena = getpass("Contraseña: ")

            autenticado, rol, bloqueado = autenticar(nombre_usuario, contrasena)
            if autenticado and rol is not None:
                input(
                    Fore.GREEN
                    + Style.BRIGHT
                    + "\nInicio de sesión exitoso, presione Enter para continuar..."
                )
                menu(rol)
                return

            if bloqueado:
                input(
                    Fore.RED
                    + Style.BRIGHT
                    + "\nDemasiados intentos. La cuenta se bloqueó temporalmente."
                    + " Presione Enter para salir..."
                )
                return
            if intento < 4:
                input(
                    Fore.RED
                    + Style.BRIGHT
                    + "\nUsuario o contraseña incorrectos. Presione Enter para continuar..."
                )

        print(Fore.RED + Style.BRIGHT + "\nSe agotaron los intentos de inicio de sesión.")
    except KeyboardInterrupt:
        print(Fore.RED + Style.BRIGHT + "\n\nSaliendo del sistema...\n")
    except sqlite3.Error:
        print(Fore.RED + Style.BRIGHT + "\nError de base de datos. No se pudo iniciar sesión.")
    except (RuntimeError, ValueError) as error:
        print(Fore.RED + Style.BRIGHT + f"\nNo se pudo completar el inicio de sesión: {error}")
    except Exception:
        print(Fore.RED + Style.BRIGHT + "\nOcurrió un error inesperado.")
