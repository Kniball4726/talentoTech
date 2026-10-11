from src.logic.menu import menu

"""
    Punto de entrada principal del programa.
    Ejecuta la función `menu()` para mostrar el menú principal del sistema de gestión de productos
    y permitir al usuario seleccionar una opción para agregar, mostrar, modificar o eliminar productos.
    Si el usuario ingresa una opción inválida, se muestra un mensaje de error y se vuelve a mostrar el menú.
    Si el usuario ingresa un valor no numérico, se muestra un mensaje de error y se vuelve a mostrar el menú.
    Si el usuario presiona Ctrl+C, se muestra un mensaje de salida y se termina la ejecución del programa.
    Parámetros:
    - Ninguno
    Retorna:
    - Ninguno
"""

if __name__ == "__main__":
    """    Ejecuta la función `menu()` para mostrar el menú principal del sistema de gestión de productos.
    """
    menu();