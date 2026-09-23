from logic.funciones import agregarProducto

global productos
productos:list = []

while True:
    print("Bienvenido al sistema de gestión de productos");
    print("1.- Agregar producto");
    print("2.- Mostrar productos");
    print("3.- Modificar producto");
    print("4.- Eliminar producto");
    print("5.- Salir");
    opcion = int(input("Seleccione una opción: "));
    
    match opcion:
        case 1:
            nombre = input("Ingrese el nombre del producto: ");
            categoria = input("Ingrese la categoría del producto: ");
            precio = float(input("Ingrese el precio del producto: "));

            producto = {
                "nombre": nombre,
                "categoria": categoria,
                "precio": precio
            }

            productos.append(producto);
            print("Producto agregado correctamente");
            print(productos);

        case 2:
            if len(productos) == 0:
                print("No hay productos registrados");  
            else:
                print("Productos registrados:");
                for producto in productos:
                    print(f"Nombre: {producto['nombre']}, Categoría: {producto['categoria']}, Precio: {producto['precio']}]");


