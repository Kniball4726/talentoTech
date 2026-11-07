from src.logic.productos import limpiar_pantalla
from src.logic.usuarios import agregar_usuario, mostrar_usuarios, modificar_usuario, eliminar_usuario   
from colorama import Style, Fore, Back, init
import sqlite3
import src.data.conectar as db

init(autoreset=True)

def menu_usuarios():
    limpiar_pantalla();
    try:
        while True:
            limpiar_pantalla();
            print(Fore.YELLOW+Style.BRIGHT+"=================================================");
            print(Fore.GREEN+Style.BRIGHT+"Bienvenido al sistema de gestión de usuarios");
            print(Fore.YELLOW+Style.BRIGHT+"=================================================");
            print("1.- Agregar usuario");
            print("2.- Mostrar usuarios");
            print("3.- Modificar usuario");
            print("4.- Eliminar usuario");
            print("0.- Volver al menú principal");

            opcion: int = int(input(Fore.GREEN+Style.BRIGHT+"\nSeleccione una opción: "));

            match opcion:
                case 1:
                    agregar_usuario();
                case 2:
                    mostrar_usuarios();
                case 3:
                    modificar_usuario();
                case 4:
                    eliminar_usuario();
                case 0:
                    return
                case _:
                    input("Opción inválida, por favor seleccione una opción válida");
    except ValueError:
        print(Fore.RED+Style.BRIGHT+"\nError: Ingrese un valor numérico válido.");
        input("\nPresione Enter para continuar...");
    except KeyboardInterrupt:
        print(Fore.RED+Style.BRIGHT+"\n\nSaliendo del sistema...\n");
    except Exception as e:
        print(Fore.RED+Style.BRIGHT+f"\nError inesperado: {e}");
        input("\nPresione Enter para continuar...");