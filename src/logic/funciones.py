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
    print("Producto agregado correctamente")

def mostrar_productos():
    limpiar_pantalla()  
    print("Mostrar productos\n");
    if len(productos) == 0:
        print("No hay productos registrados");  
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
    else:
        nombre: str = input("Ingrese el nombre del producto a modificar: ").capitalize().strip();
        for producto in productos:
            if producto["nombre"] == nombre:
                categoria: str = input("Ingrese la nueva categoría del producto: ").capitalize().strip();
                precio: float = float(input("Ingrese el nuevo precio del producto: "));
                producto["categoria"] = categoria;
                producto["precio"] = precio;
                input("Producto modificado correctamente");
            else:
                print("Producto no encontrado");        

def eliminar_producto():
    limpiar_pantalla()
    print("Eliminar producto\n");
    if len(productos) == 0:
        print("No hay productos registrados");
    else:
        nombre: str = input("Ingrese el nombre del producto a eliminar: ").capitalize().strip();
        for producto in productos:
            if producto["nombre"] == nombre:
                productos.remove(producto);
                input("Producto eliminado correctamente");
            else:
                input("Producto no encontrado");
