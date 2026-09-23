import os

productos:list = []

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def agregar_producto():
    limpiar_pantalla()
    print("Agregar producto\n");
    nombre: str = input("Ingrese el nombre del producto: ").capitalize().strip()
    categoria: str = input("Ingrese la categoría del producto: ").capitalize().strip()
    precio: float = float(input("Ingrese el precio del producto: "))

    producto: dict = {
        "nombre": nombre,
        "categoria": categoria,
        "precio": precio
    }

    productos.append(producto)
    print("\nProducto agregado correctamente")
    respuesta: str = input("\nDesea introducir otro producto? (s/n): ")
    if respuesta.lower() == 's':
        agregar_producto()
    else:
        input("\nRegresando al menú principal...")

def mostrar_productos():
    limpiar_pantalla()  
    print("Mostrar productos\n");
    if len(productos) == 0:
        print("No hay productos registrados");  
        input("\nPresione Enter para continuar...");
    else:
        print("Productos registrados:");
        contador: int = 1
        for producto in productos:
            print(f"\nIndice: {contador}\nNombre: {producto['nombre']}\nCategoría: {producto['categoria']}\nPrecio: {producto['precio']}\n");
            contador += 1
        input("\nPresione Enter para continuar...");

def modificar_producto():
    limpiar_pantalla()
    print("Modificar producto\n");
    if len(productos) == 0:
        print("No hay productos registrados");
        input("\nPresione Enter para continuar...");
    else:
        mostrar_productos()
        indice: int = int(input("\nIngrese el indice del producto a modificar: "));
        if (indice < 1 or indice > len(productos)):
            print("No se ha ingresado un indice válido");
            input("\nPresione Enter para continuar...");
        else:
            producto = productos[indice - 1]
            nombre: str = input("\nIngrese el nuevo nombre del producto: ").capitalize().strip();
            categoria: str = input("Ingrese la nueva categoría del producto: ").capitalize().strip();
            precio: float = float(input("Ingrese el nuevo precio del producto: "));

            producto["nombre"] = nombre;    
            producto["categoria"] = categoria;
            producto["precio"] = precio;
            print("\nProducto modificado correctamente");
            input("\nPresione Enter para continuar...");




def eliminar_producto():
    limpiar_pantalla()
    print("Eliminar producto\n");
    mostrar_productos()
    if len(productos) == 0:
        print("No hay productos registrados");
    else:
        indice: int = int(input("Ingrese el índice del producto a eliminar: "));
        if 1 <= indice <= len(productos):
            producto = productos[indice - 1]
            productos.remove(producto);
            print("\nProducto eliminado correctamente");
            input("\nPresione Enter para continuar...");
            return;
        else:
            print("\nProducto no encontrado");
            input("\nPresione Enter para continuar...");
