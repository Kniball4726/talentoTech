from src.logic.funciones import agregar_producto, mostrar_productos, modificar_producto, eliminar_producto, limpiar_pantalla

global productos
productos:list = []

def menu():
    limpiar_pantalla();
    try:
        while True:
            limpiar_pantalla();
            print("Bienvenido al sistema de gestión de productos");
            print("1.- Agregar producto");
            print("2.- Mostrar productos");
            print("3.- Modificar producto");
            print("4.- Eliminar producto");
            print("5.- Salir");
            opcion: int = int(input("Seleccione una opción: "));
            
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
                    print("Saliendo del sistema...");
                    break;
                case _:
                    print("Opción inválida, por favor seleccione una opción válida");

    except ValueError:
        print("Error: Debe ingresar un número entero para seleccionar una opción");
    except KeyboardInterrupt:
        print("\nSaliendo del sistema...");
    except Exception as e:
        print(f"\nError inesperado: {e}");


