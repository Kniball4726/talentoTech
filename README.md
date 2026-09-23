# Sistema de Gestión de Productos

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/Status-Funcional-success?style=for-the-badge)

</div>

## Descripción del proyecto

Este proyecto consiste en una aplicación de consola desarrollada en Python para gestionar productos de manera simple, ordenada y eficiente. Su finalidad es facilitar la administración básica de un inventario, permitiendo registrar, consultar, actualizar y eliminar productos sin necesidad de una base de datos externa.

La aplicación ofrece una interfaz interactiva en consola, ideal para aprender lógica de programación, manejo de listas y validación de datos en Python.

## Objetivo

Crear una herramienta práctica para administrar un inventario básico, que permita llevar un control sencillo de productos, precios y categorías en un entorno de consola.

## Funcionalidades principales

- Registrar nuevos productos
- Consultar la lista completa de productos
- Modificar la categoría y el precio de un producto
- Eliminar productos del inventario
- Salir del sistema de manera segura

## Tecnologías utilizadas

- Python 3
- Listas y diccionarios
- Menú interactivo por consola
- Lógica de control de flujo

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

## Cómo usar la aplicación

Al iniciar el programa, aparecerá un menú con estas opciones:

1. Agregar producto
2. Mostrar productos
3. Modificar producto
4. Eliminar producto
0. Salir

Debe ingresar la opción deseada y seguir las instrucciones que aparecen en pantalla.

## Estructura del proyecto

```text
talentoTech/
├── main.py
├── README.md
├── requirements.txt
└── src/
    └── logic/
        ├── funciones.py
        └── menu.py
```

### Archivos principales

- `main.py`: punto de entrada del sistema
- `src/logic/funciones.py`: contiene la lógica de gestión de productos
- `src/logic/menu.py`: define la interfaz del menú principal
- `requirements.txt`: lista de dependencias del proyecto

## Observaciones

Este proyecto implementa una gestión básica de inventario en memoria. Los datos se mantienen mientras la aplicación está en ejecución y no incluyen almacenamiento persistente en base de datos ni archivos externos.

## Autor

Gregory Rodriguez

## Estado del proyecto

Proyecto funcional y en desarrollo, orientado a la gestión básica de productos mediante una interfaz de consola.
