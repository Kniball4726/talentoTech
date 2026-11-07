from src.logic.productos import agregar_producto, mostrar_productos, modificar_producto, eliminar_producto, limpiar_pantalla
from colorama import Fore, Back, Style, init

init(autoreset=True)



"""    Función que muestra el menú principal del sistema de gestión de productos.
    Permite al usuario seleccionar una opción para agregar, mostrar, modificar o eliminar productos.
    Si el usuario ingresa una opción inválida, se muestra un mensaje de error y se vuelve a mostrar el menú.
    Si el usuario ingresa un valor no numérico, se muestra un mensaje de error y se vuelve a mostrar el menú.
    Si el usuario presiona Ctrl+C, se muestra un mensaje de salida y se termina la ejecución del programa.
    
    Parámetros:
    - Ninguno
    Retorna:
    - Ninguno
"""
def menu(rol: str):
    limpiar_pantalla();
    try:
        while True:
            limpiar_pantalla();
            print(Fore.YELLOW+Style.BRIGHT+"=================================================");
            print(Fore.GREEN+Style.BRIGHT+"Bienvenido al sistema de gestión de productos");
            print(Fore.YELLOW+Style.BRIGHT+"=================================================");
            print("1.- Agregar producto");
            print("2.- Mostrar productos");
            print("3.- Modificar producto");
            print("4.- Eliminar producto");
            if rol != "Admin":
               print("0.- Salir");
            else:
                print("5.- Gestionar usuarios");
                print("0.- Salir");

            opcion: int = int(input(Fore.GREEN+Style.BRIGHT+"\nSeleccione una opción: "));

            match opcion:
                case 1:
                    agregar_producto();
                case 2:
                    mostrar_productos();
                case 3:
                    modificar_producto();
                case 4:
                    eliminar_producto();
                case 5:
                    if rol == "Admin":
                        from src.gui.usuarios import menu_usuarios
                        menu_usuarios();
                    else:
                        print(Fore.RED+Style.BRIGHT+"\nError: Opción inválida. Solo los administradores pueden gestionar usuarios.");
                        input("\nPresione Enter para continuar...");
                case 0:
                    print("Saliendo del sistema...");
                    break;
                case _:
                    print("Opción inválida, por favor seleccione una opción válida");

    except ValueError:
        input(Fore.RED+Style.BRIGHT+"\nError: Debe ingresar un número entero para seleccionar una opción");
        menu(rol);
    except KeyboardInterrupt:
        print(Fore.RED+Style.BRIGHT+"\n\nSaliendo del sistema...\n");
    except Exception as e:
        print(Fore.RED+Style.BRIGHT+f"\nError inesperado: {e}");
