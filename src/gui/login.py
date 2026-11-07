from colorama import Fore, Style, Back, init
from src.logic.productos import limpiar_pantalla, loguear
from src.gui.principal import menu

init(autoreset=True)

veces:int = 0;

def login():
    try:
        limpiar_pantalla()
        print(Fore.YELLOW+Style.BRIGHT+"=====================================================")
        print(Fore.GREEN+Style.BRIGHT+"Hola, bienvenido al sistema de gestión de productos")
        print(Fore.YELLOW+Style.BRIGHT+"=====================================================")
        print("\nIndique su usuario y contraseña para continuar (presione Enter para continuar)")
        nombre_usuario: str = input("\nUsuario: ").strip().capitalize()
        contrasena: str = input("Contraseña: ").strip().capitalize()

    
        autenticado, rol = loguear(nombre_usuario, contrasena)
        if autenticado and rol is not None:
            input(Fore.GREEN+Style.BRIGHT+"\nInicio de sesión exitoso, presione Enter para continuar...")
            menu(rol)
        else:
            global veces
            if veces == 3:
                input(Fore.RED+Style.BRIGHT+"\nHa excedido el número máximo de intentos, presione Enter para salir...")
                exit()
            else:
                input(Fore.RED+Style.BRIGHT+"\nUsuario o contraseña incorrectos, presione Enter para continuar...")
                veces += 1;
                login()

    except Exception as e:
        input(Fore.RED+Style.BRIGHT+f"\nError inesperado: {e}, presione Enter para continuar...")
        login()
    except KeyboardInterrupt:
        print(Fore.RED+Style.BRIGHT+"\n\nSaliendo del sistema...\n")


