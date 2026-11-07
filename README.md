# TalentoTech

Sistema de inventario de consola desarrollado con Python y SQLite. Este documento incluye el manual de uso por rol y una guía para desarrolladores.

## Manual de usuario

### Inicio de sesión

1. Ejecuta la aplicación y escribe tu nombre de usuario y contraseña.
2. En una base de datos nueva, la aplicación crea una cuenta inicial si aún no existe:
   - Usuario: `Admin`
   - Contraseña: `Admin`
3. No uses las credenciales iniciales en entornos compartidos o con datos sensibles.

Después de iniciar sesión se muestra el menú principal. Todos los usuarios pueden operar con productos; las cuentas con rol `Admin` también tienen acceso a la gestión de usuarios.

### Funciones disponibles para `Usuario` y `Admin`

En el menú principal:

1. **Agregar producto:** ingresa nombre, descripción, cantidad, categoría y precio.
2. **Mostrar productos:** consulta los productos y sus ID.
3. **Modificar producto:** ingresa el ID del producto y los nuevos valores. Presiona Enter en los campos que quieras conservar. Cantidad y precio deben ser valores numéricos no negativos.
4. **Eliminar producto:** ingresa el ID del producto que deseas borrar.
5. **Salir:** cierra el menú principal y termina la sesión.

### Funciones adicionales para `Admin`

La opción **5. Gestionar usuarios** abre el menú de usuarios:

1. **Agregar usuario:** solicita nombre, apellido, correo electrónico, contraseña y rol (`Admin` o `Usuario`).
2. **Mostrar usuarios:** lista el ID, nombre y rol de cada cuenta.
3. **Modificar usuario:** permite cambiar el nombre y el rol de una cuenta seleccionada por ID.
4. **Eliminar usuario:** elimina la cuenta seleccionada por ID.
5. **Volver al menú principal:** cierra el menú de usuarios y regresa al menú anterior.

## Manual del desarrollador

### Requisitos

- Python 3.10 o superior.
- SQLite 3, incluido en la biblioteca estándar de Python.
- Colorama para los colores de la consola.
- PyInstaller para generar un ejecutable (opcional).
- Windows, Linux o macOS.

### Preparar el entorno

Clona el repositorio y entra en su directorio:

```bash
git clone https://github.com/Kniball4726/talentoTech.git
cd talentoTech
```

Crea y activa un entorno virtual (recomendado).

Windows:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Instala las dependencias:

```bash
pip install -r requirements.txt
pip install colorama
```

Ejecuta la aplicación desde la raíz del proyecto:

```bash
python main.py
```

### Estructura del proyecto

```text
talentoTech/
├── main.py
├── main.spec
├── requirements.txt
├── README.md
└── src/
    ├── data/
    │   ├── conectar.py
    │   └── inventario.db
    ├── gui/
    │   ├── login.py
    │   ├── principal.py
    │   └── usuarios.py
    └── logic/
        ├── productos.py
        └── usuarios.py
```

- `main.py`: punto de entrada; inicia el login.
- `src/gui/login.py`: solicita credenciales y dirige al menú con el rol autenticado.
- `src/gui/principal.py`: menú de productos y acceso de administradores al menú de usuarios.
- `src/gui/usuarios.py`: menú de gestión de usuarios.
- `src/logic/productos.py`: autenticación y operaciones de inventario.
- `src/logic/usuarios.py`: operaciones de administración de cuentas.
- `src/data/conectar.py`: conexión SQLite, creación de tablas y cuenta inicial.
- `src/data/inventario.db`: base de datos local.

### Base de datos

La ruta configurada es `src/data/inventario.db`, relativa al directorio de trabajo. Ejecuta `main.py` desde la raíz para evitar que SQLite cree o busque la base en otra ubicación. Al conectarse, el programa crea las tablas si no existen.

Tabla `productos`:

| Campo           | Tipo/uso             |
| --------------- | -------------------- |
| `id`          | Identificador único |
| `nombre`      | Nombre del producto  |
| `descripcion` | Descripción         |
| `cantidad`    | Unidades disponibles |
| `precio`      | Precio               |
| `categoria`   | Categoría           |

Tabla `usuarios`:

| Campo          | Tipo/uso                |
| -------------- | ----------------------- |
| `id`         | Identificador único    |
| `nombre`     | Nombre de usuario       |
| `apellido`   | Apellido                |
| `email`      | Correo electrónico     |
| `contrasena` | Contraseña             |
| `rol`        | `Admin` o `Usuario` |

**Nota de seguridad:** la implementación actual guarda y compara contraseñas directamente en SQLite. Antes de usarla fuera de un entorno de aprendizaje, cambia este comportamiento por almacenamiento de contraseñas con hash y evita las credenciales iniciales.

### Generar un ejecutable

Desde la raíz del proyecto:

```bash
pyinstaller --onefile main.py
```

PyInstaller genera el ejecutable en `dist/`. La base de datos no se incluye automáticamente: al ejecutar el programa, debe estar disponible en `src/data/inventario.db` relativo al directorio de trabajo.

## Tecnologías

- Python
- SQLite (`sqlite3`)
- Colorama
- PyInstaller (opcional)

## Autor

Gregory Rodriguez
