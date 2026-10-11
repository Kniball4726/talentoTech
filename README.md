# TalentoTech

Sistema de gestión de productos desarrollado en Python con SQLite para llevar el control de inventario desde la consola.

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Base%20de%20datos-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Estado](https://img.shields.io/badge/Estado-En%20desarrollo-orange?style=for-the-badge)

</div>

## Descripción

TalentoTech es una aplicación de consola para administrar un inventario de productos de forma simple y persistente. Permite registrar, listar, actualizar y eliminar artículos, manteniendo la información en una base de datos local SQLite.

El proyecto está pensado como ejercicio de práctica en programación Python, estructuras de control, interacción por consola y manejo de bases de datos.

## Funcionalidades

- Registrar nuevos productos
- Mostrar todos los productos almacenados
- Modificar información de un producto existente
- Eliminar productos del inventario
- Guardar datos de forma persistente en SQLite
- Menú interactivo para gestión rápida desde terminal

## Tecnologías

- Python 3
- SQLite 3
- `sqlite3` (módulo de Python para la base de datos)
- Menú por consola interactivo
- PyInstaller (opcional, para empaquetar la aplicación)

## Requisitos

- Python 3.8 o superior
- Sistema operativo: Windows, Linux o macOS
- Terminal o consola de comandos

## Instalación

1. Clona el repositorio:

   ```bash
   git clone https://github.com/Kniball4726/talentoTech.git
   ```

2. Entra en la carpeta del proyecto:

   ```bash
   cd talentoTech
   ```

3. Crea y activa un entorno virtual (recomendado):

   Windows:

   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate
   ```

   Linux/macOS:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

4. Instala las dependencias del proyecto:

   ```bash
   pip install -r requirements.txt
   ```

5. Ejecuta la aplicación:

   ```bash
   python main.py
   ```

## Estructura del proyecto

```text
talentoTech/
├── LICENSE
├── README.md
├── main.py
├── requirements.txt
├── .gitignore
├── src/
│   ├── data/
│   │   ├── conectar.py
│   │   └── dataprod.db
│   └── logic/
│       ├── funciones.py
│       └── menu.py
└── ttech/                  # entorno virtual local (si se creó)
    └── ...
```

### Archivos principales

- `main.py`: punto de entrada de la aplicación.
- `src/data/conectar.py`: establece la conexión a la base de datos y crea la tabla `productos` si no existe.
- `src/data/dataprod.db`: base de datos local del sistema.
- `src/logic/funciones.py`: contiene la lógica para agregar, mostrar, modificar y eliminar productos.
- `src/logic/menu.py`: define el menú principal del programa.

## Uso

Al iniciar el programa, se muestra un menú con estas opciones:

1. Agregar producto
2. Mostrar productos
3. Modificar producto
4. Eliminar producto
0. Salir

El usuario debe ingresar la opción deseada y completar la información solicitada en cada operación.

## Crear un ejecutable

PyInstaller está incluido en `requirements.txt`. Después de instalar las dependencias, puedes crear el ejecutable directamente desde `main.py` desde la carpeta raíz del proyecto:

```bash
pyinstaller --onefile main.py
```

PyInstaller genera un único archivo ejecutable dentro de `dist/`: en Windows será `dist/main.exe`; en Linux o macOS será `dist/main`. La opción `--onefile` empaqueta la aplicación en un solo archivo y conserva la consola, necesaria para interactuar con el menú.

PyInstaller genera el ejecutable para el sistema operativo en el que se ejecuta; para distribuirlo en otro sistema operativo, debes volver a generarlo allí.

## Modelo de datos

La base de datos SQLite almacena los productos en la tabla `productos` con la siguiente estructura:

- `id`: identificador único
- `nombre`: nombre del producto
- `categoria`: categoría a la que pertenece
- `precio`: valor del producto

## Estado del proyecto

Este proyecto se encuentra en desarrollo como una herramienta funcional básica de inventario para consola, con persistencia local mediante SQLite.

## Autor

Gregory Rodriguez
