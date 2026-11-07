from colorama import Fore, Back, Style, init
import sqlite3
import os
import src.data.conectar as db
from src.logic.autenticacion import autenticar

productos:list = []

init(autoreset=True)

def limpiar_pantalla():
    """
    Función para limpiar la pantalla de la consola.
    Detecta el sistema operativo y ejecuta el comando correspondiente para limpiar la pantalla.
    
    Parámetros:
    - Ninguno
    Retorna:
    - Ninguno"""
    os.system('cls' if os.name == 'nt' else 'clear')

def loguear(username, password):
    """
    Función para autenticar a un usuario en el sistema.
    Compara el nombre de usuario y la contraseña ingresados con los registros de la base de datos.
    
    Parámetros:
    - username: Nombre de usuario ingresado por el usuario
    - password: Contraseña ingresada por el usuario
    Retorna:
    - True si la autenticación es exitosa, False en caso contrario
    """
    autenticado, rol, _ = autenticar(username, password)
    return autenticado, rol
    
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
    try:
        limpiar_pantalla()
        print(Fore.YELLOW+Style.BRIGHT+"===================")
        print(Fore.GREEN+Style.BRIGHT+"Agregar producto")
        print(Fore.YELLOW+Style.BRIGHT+"===================")
        nombre: str = input("\nIngrese el nombre del producto: ").capitalize().strip()
        descripcion: str = input("Ingrese la descripción del producto: ").capitalize().strip()
        cantidad: int = int(input("Ingrese la cantidad del producto: "))
        categoria: str = input("Ingrese la categoría del producto: ").capitalize().strip()
        precio: float = float(input("Ingrese el precio del producto: "))

        conexion = db.conectar()

        if conexion is not None:
            cursor = conexion.cursor()
            cursor.execute(
                "INSERT INTO productos (nombre, descripcion, cantidad, categoria, precio) VALUES (?, ?, ?, ?, ?)",
                (nombre, descripcion, cantidad, categoria, precio)
            )
            conexion.commit()
            print("\nProducto agregado correctamente")
    except sqlite3.Error as e:
        conexion.rollback()
        print(f"\nError al guardar el producto: {e}")
    except ValueError:
        print(Fore.RED+Style.BRIGHT+"\nError: Debe ingresar un número válido para la cantidad y el precio")
    except Exception as e:
        print(Fore.RED+Style.BRIGHT+f"\nError inesperado: {e}")
    except KeyboardInterrupt:
        print(Fore.RED+Style.BRIGHT+"\n\nSaliendo del sistema...\n")
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
    try:
        limpiar_pantalla()  
        print(Fore.YELLOW+Style.BRIGHT+"====================")
        print(Fore.GREEN+Style.BRIGHT+"Mostrar productos")
        print(Fore.YELLOW+Style.BRIGHT+"====================")

        conexion = db.conectar();
        
        if conexion is None:
            print(Fore.RED+Style.BRIGHT+"No se pudo conectar a la base de datos.")
            input("\nPresione Enter para continuar...")
            return
        else:
            consulta = conexion.execute("SELECT * FROM productos")
            registros = consulta.fetchall()
            if len(registros) == 0:
                print(Fore.RED+Style.BRIGHT+"No hay productos registrados")
                input("\nPresione Enter para continuar...")
                return
            else:
                for fila in registros:
                    print(f"id: {fila[0]}\nNombre: {fila[1]}\nCategoría: {fila[5]}\nDescripción: {fila[2]}\nCantidad: {fila[3]}\nPrecio: {fila[4]}\n=========================")
                input("\nPresione Enter para continuar...")
    except sqlite3.Error as e:
        print(Fore.RED+Style.BRIGHT+f"Error al obtener los productos: {e}")
        input("\nPresione Enter para continuar...")
    except Exception as e:
        print(Fore.RED+Style.BRIGHT+f"\nError inesperado: {e}")
        input("\nPresione Enter para continuar...")
    except KeyboardInterrupt:
        print(Fore.RED+Style.BRIGHT+"\n\nSaliendo del sistema...\n")
    finally:
        db.cerrar_conexion(conexion)

def modificar_producto():
    """
    Modifica los datos de un producto seleccionado por su identificador.
    Dejar un campo vacío conserva su valor actual.
    """
    try:
        limpiar_pantalla()
        print(Fore.YELLOW+Style.BRIGHT+"=====================")
        print(Fore.GREEN+Style.BRIGHT+"Modificar producto")
        print(Fore.YELLOW+Style.BRIGHT+"=====================")

        conexion = db.conectar()

        if not conexion:
            print(Fore.RED+Style.BRIGHT+"No se pudo conectar a la base de datos.")
            input("\nPresione Enter para continuar...")

        productos = conexion.execute(
            "SELECT id, nombre, descripcion, cantidad, categoria, precio "
            "FROM productos ORDER BY id"
        ).fetchall()

        if not productos:
            print(Fore.RED+Style.BRIGHT+"No hay productos registrados.")
            input("\nPresione Enter para continuar...")
            return

        for producto in productos:
            print(
                f"id: {producto[0]} | Nombre: {producto[1]} | "
                f"Descripción: {producto[2]} | Cantidad: {producto[3]} | "
                f"Categoría: {producto[4]} | Precio: {producto[5]}"
            )

        producto_id = int(input("\nIngrese el ID del producto a modificar: "))
        producto = conexion.execute(
            "SELECT nombre, descripcion, cantidad, categoria, precio "
            "FROM productos WHERE id = ?",
            (producto_id,),
        ).fetchone()
        if producto is None:
            print(Fore.RED+Style.BRIGHT+"\nNo se encontró un producto con ese ID.")
            input("\nPresione Enter para continuar...")
            return

        nombre = input(f"Nombre [{producto[0]}]: ").strip() or producto[0]
        descripcion = input(f"Descripción [{producto[1]}]: ").strip() or producto[1]
        cantidad_ingresada = input(f"Cantidad [{producto[2]}]: ").strip()
        cantidad = int(cantidad_ingresada) if cantidad_ingresada else producto[2]
        categoria = input(f"Categoría [{producto[3]}]: ").strip() or producto[3]
        precio_ingresado = input(f"Precio [{producto[4]}]: ").strip()
        precio = float(precio_ingresado) if precio_ingresado else producto[4]

        if cantidad < 0 or precio < 0:
            raise ValueError("La cantidad y el precio no pueden ser negativos.")

        conexion.execute(
            "UPDATE productos "
            "SET nombre = ?, descripcion = ?, cantidad = ?, categoria = ?, precio = ? "
            "WHERE id = ?",
            (nombre, descripcion, cantidad, categoria, precio, producto_id),
        )
        conexion.commit()
        print(Fore.GREEN+Style.BRIGHT+f"\nProducto modificado correctamente.")
        input("\nPresione Enter para continuar...")
    except ValueError:
        print(
            Fore.RED+Style.BRIGHT
            +"\nError: El ID, la cantidad y el precio deben ser valores válidos y no negativos."
        )
        input("\nPresione Enter para continuar...")
    except KeyboardInterrupt:
        print(Fore.RED+Style.BRIGHT+"\n\nOperación cancelada.\n")
    except sqlite3.Error as e:
        if conexion is not None:
            conexion.rollback()
        print(Fore.RED+Style.BRIGHT+f"\nError al modificar el producto: {e}")
        input("\nPresione Enter para continuar...")
    except Exception as e:
        print(Fore.RED+Style.BRIGHT+f"\nError inesperado: {e}")
        input("\nPresione Enter para continuar...")
    finally:
        db.cerrar_conexion(conexion)



def eliminar_producto():
    """Elimina de la base de datos el producto seleccionado por su identificador."""
    conexion = None
    try:
        limpiar_pantalla()
        print(Fore.YELLOW+Style.BRIGHT+"=====================")
        print(Fore.GREEN+Style.BRIGHT+"Eliminar producto")
        print(Fore.YELLOW+Style.BRIGHT+"=====================")

        conexion = db.conectar()
        if conexion is None:
            print(Fore.RED+Style.BRIGHT+"No se pudo conectar a la base de datos.")
            input("\nPresione Enter para continuar...")
            return

        productos = conexion.execute(
            "SELECT id, nombre, descripcion, cantidad, categoria, precio "
            "FROM productos ORDER BY id"
        ).fetchall()
        if not productos:
            print(Fore.RED+Style.BRIGHT+"No hay productos registrados.")
            input("\nPresione Enter para continuar...")
            return

        for producto in productos:
            print(
                f"id: {producto[0]} | Nombre: {producto[1]} | "
                f"Descripción: {producto[2]} | Cantidad: {producto[3]} | "
                f"Categoría: {producto[4]} | Precio: {producto[5]}"
            )

        producto_id = int(input("\nIngrese el ID del producto a eliminar: "))
        cursor = conexion.execute(
            "DELETE FROM productos WHERE id = ?",
            (producto_id,),
        )
        if cursor.rowcount == 0:
            print(Fore.RED+Style.BRIGHT+"\nNo se encontró un producto con ese ID.")
        else:
            conexion.commit()
            print(Fore.GREEN+Style.BRIGHT+f"\nProducto eliminado correctamente.")
        input("\nPresione Enter para continuar...")
    except ValueError:
        print(Fore.RED+Style.BRIGHT+"\nError: Ingrese un ID de producto válido.")
        input("\nPresione Enter para continuar...")
    except KeyboardInterrupt:
        if conexion is not None:
            conexion.rollback()
        print(Fore.RED+Style.BRIGHT+"\n\nOperación cancelada.\n")
    except sqlite3.Error as e:
        if conexion is not None:
            conexion.rollback()
        print(Fore.RED+Style.BRIGHT+f"\nError al eliminar el producto: {e}")
        input("\nPresione Enter para continuar...")
    except Exception as e:
        print(Fore.RED+Style.BRIGHT+f"\nError inesperado: {e}")
        input("\nPresione Enter para continuar...")
    finally:
        db.cerrar_conexion(conexion)