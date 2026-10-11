from src.logic.funciones import agregar_producto, mostrar_productos, modificar_producto, eliminar_producto, limpiar_pantalla


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
def menu():
    limpiar_pantalla();
    try:
        while True:
            limpiar_pantalla();
            print("Bienvenido al sistema de gestión de productos\n");
            print("1.- Agregar producto");
            print("2.- Mostrar productos");
            print("3.- Modificar producto");
            print("4.- Eliminar producto");
            print("0.- Salir");
            opcion: int = int(input("\nSeleccione una opción: "));
            
            match opcion:
                case 1:
                    agregar_producto();
                case 2:
                    mostrar_productos();
                case 3:
                    modificar_producto();
                case 4:
                    eliminar_producto();
                case 0:
                    print("Saliendo del sistema...");
                    break;
                case _:
                    print("Opción inválida, por favor seleccione una opción válida");

    except ValueError:
        input("\nError: Debe ingresar un número entero para seleccionar una opción");
        menu();
    except KeyboardInterrupt:
        print("\n\nSaliendo del sistema...\n");
    except Exception as e:
        print(f"\nError inesperado: {e}");


