import os
import sqlite3
import src.data.conectar as db



productos:list = []
conexion = db.conectar()

def limpiar_pantalla():
    """
    Función para limpiar la pantalla de la consola.
    Detecta el sistema operativo y ejecuta el comando correspondiente para limpiar la pantalla.
    
    Parámetros:
    - Ninguno
    Retorna:
    - Ninguno"""
    os.system('cls' if os.name == 'nt' else 'clear')

def agregar_producto():
    """
    Función para agregar un nuevo producto a la base de datos.
    Solicita al usuario que ingrese el nombre, categoría y precio del producto.
    Luego, guarda el producto en la base de datos y pregunta al usuario si desea agregar otro producto.
    Si el usuario responde 's', se llama recursivamente a la función para agregar otro producto.
    Si el usuario responde 'n', se muestra un mensaje indicando que se regresará al menú principal.
    
    Parámetros:
    - Ninguno
    Retorna:
    - Ninguno
    """
    limpiar_pantalla()
    print("===================")
    print("Agregar producto")
    print("===================")
    nombre: str = input("\nIngrese el nombre del producto: ").capitalize().strip()
    categoria: str = input("Ingrese la categoría del producto: ").capitalize().strip()
    precio: float = float(input("Ingrese el precio del producto: "))

    
    if conexion is not None:
        try:
            conexion.execute(
                "INSERT INTO productos (nombre, categoria, precio) VALUES (?, ?, ?)",
                (nombre, categoria, precio),
            )
            conexion.commit()
            print("\nProducto agregado correctamente")
        except sqlite3.Error as e:
            conexion.rollback()
            print(f"\nError al guardar el producto: {e}")
        finally:
            db.cerrar_conexion(conexion)

    
    respuesta: str = input("\nDesea introducir otro producto? (s/n): ")
    if respuesta.lower() == 's':
        agregar_producto()
    else:
        input("\nRegresando al menú principal...")

def mostrar_productos():
    """
    Función para mostrar todos los productos registrados en la base de datos.
    Si no hay productos registrados, se muestra un mensaje indicando que no hay productos.
    Si hay productos registrados, se muestran los detalles de cada producto (id, nombre, categoría y precio).
    Al finalizar, se espera a que el usuario presione Enter para continuar.
    
    Parámetros:
    - Ninguno
    Retorna:
    - Ninguno
    """
    limpiar_pantalla()  
    print("====================")
    print("Mostrar productos");
    print("====================")
    try:
        conexion = db.conectar()
        if conexion is None:
            print("No se pudo conectar a la base de datos.")
            return
        else:
            consulta = conexion.execute("SELECT * FROM productos")
            registros = consulta.fetchall()
            if len(registros) == 0:
                print("No hay productos registrados")
                input("\nPresione Enter para continuar...")
                return
            else:
                for fila in registros:
                    print(f"id: {fila[0]}\nNombre: {fila[1]}\nCategoría: {fila[2]}\nPrecio: {fila[3]}\n")
                input("\nPresione Enter para continuar...")
    except sqlite3.Error as e:
        print(f"Error al obtener los productos: {e}")

def modificar_producto():
    """
    Función para modificar un producto existente en la base de datos.
    Primero, se muestra la lista de productos registrados. Si no hay productos, se muestra un mensaje indicando que no hay productos registrados y se espera a que el usuario presione Enter para continuar.
    Si hay productos registrados, se solicita al usuario que ingrese el índice del producto a modificar y se valida que el índice sea válido. Si el índice es válido, se solicita al usuario que ingrese los nuevos valores para el nombre, categoría y precio del producto.
    Luego, se actualiza el producto en la base de datos y se muestra un mensaje indicando que el producto fue modificado correctamente.
    Si el índice no es válido, se muestra un mensaje indicando que no se ha ingresado un índice válido y se espera a que el usuario presione Enter para continuar.
    
    Parámetros: Ninguno
    Retorna: Ninguno
    
    """
    limpiar_pantalla()
    print("=====================")
    print("Modificar producto");
    print("=====================")
    if len(db.obtener_productos()) == 0:
        print("No hay productos registrados");
        input("\nPresione Enter para continuar...");
    else:
        mostrar_productos()
        indice: int = int(input("\nIngrese el indice del producto a modificar: "));
        if (indice < 1 or indice > len(db.obtener_productos())):
            print("No se ha ingresado un indice válido");
            input("\nPresione Enter para continuar...");
        else:
            producto = db.obtener_productos()[indice - 1]
            nombre: str = input("\nIngrese el nuevo nombre del producto: ").capitalize().strip();
            categoria: str = input("Ingrese la nueva categoría del producto: ").capitalize().strip();
            precio: float = float(input("Ingrese el nuevo precio del producto: "));

            producto["nombre"] = nombre;    
            producto["categoria"] = categoria;
            producto["precio"] = precio;
            print("\nProducto modificado correctamente");
            input("\nPresione Enter para continuar...");



def eliminar_producto():
    """
    Función para eliminar un producto existente en la base de datos.
    Primero, se muestra la lista de productos registrados. Si no hay productos, se muestra un mensaje indicando que no hay productos registrados y se espera a que el usuario presione Enter para continuar.
    Si hay productos registrados, se solicita al usuario que ingrese el índice del producto a eliminar y se valida que el índice sea válido. Si el índice es válido, se elimina el producto de la base de datos y se muestra un mensaje indicando que el producto fue eliminado correctamente.
    Si el índice no es válido, se muestra un mensaje indicando que no se ha ingresado un índice válido y se espera a que el usuario presione Enter para continuar.
    
    Parámetros: Ninguno
    Retorna: Ninguno
    """
    limpiar_pantalla()
    print("=====================")
    print("Eliminar producto");
    print("=====================")
    mostrar_productos()
    if len(db.obtener_productos()) == 0:
        print("No hay productos registrados");
        input("\nPresione Enter para continuar...");
    else:
        indice: int = int(input("Ingrese el índice del producto a eliminar: "));
        if 1 <= indice <= len(db.obtener_productos()):
            producto = db.obtener_productos()[indice - 1]
            db.eliminar_producto(producto);
            print("\nProducto eliminado correctamente");
            input("\nPresione Enter para continuar...");
            return;
        else:
            print("\nProducto no encontrado");
            input("\nPresione Enter para continuar...");
