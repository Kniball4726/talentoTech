# TalentoTech - Sistema de gestión de productos

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Base%20de%20datos-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Status](https://img.shields.io/badge/Estado-Funcional-success?style=for-the-badge)

</div>

## Descripción del proyecto

TalentoTech es una aplicación de consola desarrollada en Python para gestionar un inventario de productos de forma simple y ordenada. El sistema permite registrar, consultar, actualizar y eliminar elementos, con persistencia de datos mediante SQLite.

La aplicación está pensada para practicar lógica de programación, manejo de bases de datos y desarrollo de menús interactivos en consola.

## Objetivo

Crear una herramienta práctica para administrar productos, categorías y precios, manteniendo la información guardada de forma persistente sin necesidad de un servicio externo.

## Funcionalidades principales

- Agregar nuevos productos
- Mostrar todos los productos registrados
- Modificar información de un producto
- Eliminar productos del inventario
- Mantener los datos persistentes en SQLite
- Salir del sistema de forma segura

## Tecnologías utilizadas

- Python 3
- SQLite 3
- Conexión a base de datos con `sqlite3`
- Menú interactivo por consola

## Requisitos del sistema

- Python 3.8 o superior
- Sistema operativo Windows, Linux o macOS
- Terminal o consola de comandos

## Instalación

1. Clona este repositorio:

   ```bash
   git clone https://github.com/Kniball4726/talentoTech.git
   ```

2. Accede a la carpeta del proyecto:

   ```bash
   cd talentoTech
   ```

3. Crea un entorno virtual (opcional, pero recomendado):

   ```bash
   python -m venv .venv
   ```

4. Activa el entorno virtual:

   - Windows:

     ```bash
     .\.venv\Scripts\activate
     ```

   - Linux/macOS:

     ```bash
     source .venv/bin/activate
     ```

5. Ejecuta la aplicación:

   ```bash
   python main.py
   ```

> No se requieren dependencias externas adicionales, ya que la lógica se implementa con la librería estándar de Python y SQLite.

## Uso de la aplicación

Al iniciar el programa, se mostrará un menú con las siguientes opciones:

1. Agregar producto
2. Mostrar productos
3. Modificar producto
4. Eliminar producto
0. Salir

Debes ingresar la opción deseada y seguir las instrucciones que aparecen en pantalla.

## Estructura del proyecto

```text
talentoTech/
├── main.py
├── README.md
├── src/
│   ├── data/
│   │   ├── conectar.py
│   │   └── dataprod.db
│   └── logic/
│       ├── funciones.py
│       └── menu.py
└── ttech/
    └── Scripts/   (entorno virtual local)
```

### Archivos principales

- `main.py`: punto de entrada de la aplicación
- `src/data/conectar.py`: gestiona la conexión a SQLite y crea la tabla `productos`
- `src/data/dataprod.db`: base de datos local del sistema
- `src/logic/funciones.py`: contiene la lógica para agregar, consultar, modificar y eliminar productos
- `src/logic/menu.py`: define la interfaz del menú principal

## Persistencia de datos

La información se guarda en la base de datos SQLite ubicada en `src/data/dataprod.db`. La tabla `productos` incluye los siguientes campos:

- `id`
- `nombre`
- `categoria`
- `precio`

## Observaciones

Este proyecto implementa una gestión básica de inventario con almacenamiento persistente en base de datos local. La aplicación está orientada a consola y se usa como ejercicio de programación con Python y SQLite.

## Autor

Gregory Rodriguez

## Estado del proyecto

Proyecto funcional en desarrollo, con gestión básica de productos mediante consola y persistencia en SQLite.
