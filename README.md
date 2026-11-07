# TalentoTech

Sistema de inventario de consola desarrollado con Python y SQLite. Este documento incluye el manual de uso por rol y una guía para desarrolladores.

## Manual de usuario

### Inicio de sesión

1. Ejecuta la aplicación.
2. La primera vez que se ejecuta con una base de datos vacía, solicita los datos de la primera cuenta administradora. Elige una contraseña única de entre 12 y 1024 caracteres y confírmala.
3. Escribe el nombre de usuario y la contraseña. La contraseña no se muestra en pantalla.
4. Después de cinco intentos fallidos para un nombre de usuario, los intentos para ese nombre se bloquean durante un minuto.

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

1. **Agregar usuario:** solicita nombre, apellido, correo electrónico, contraseña de entre 12 y 1024 caracteres y rol (`Admin` o `Usuario`). La contraseña debe confirmarse.
2. **Mostrar usuarios:** lista el ID, nombre y rol de cada cuenta.
3. **Modificar usuario:** permite cambiar el nombre y el rol de una cuenta seleccionada por ID.
4. **Eliminar usuario:** elimina la cuenta seleccionada por ID.
5. **Volver al menú principal:** cierra el menú de usuarios y regresa al menú anterior.

No se puede degradar ni eliminar al último administrador. Los nombres de usuario no distinguen mayúsculas de minúsculas y no pueden repetirse.

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

En un primer inicio, crea la cuenta administradora cuando la aplicación lo solicite. No hay credenciales iniciales compartidas.

Para ejecutar las pruebas:

```bash
python -m unittest discover -s tests -v
```

### Estructura del proyecto

```text
talentoTech/
├── main.py
├── main.spec
├── requirements.txt
├── README.md
├── tests/
│   └── test_autenticacion.py
└── src/
    ├── data/
    │   ├── conectar.py
    │   └── inventario.db (generada localmente; no se versiona)
    ├── gui/
    │   ├── login.py
    │   ├── principal.py
    │   └── usuarios.py
    └── logic/
        ├── autenticacion.py
        ├── productos.py
        └── usuarios.py
```

- `main.py`: punto de entrada; inicia el login.
- `src/gui/login.py`: configura la cuenta inicial si hace falta, solicita las credenciales y dirige al menú con el rol autenticado.
- `src/gui/principal.py`: menú de productos y acceso de administradores al menú de usuarios.
- `src/gui/usuarios.py`: menú de gestión de usuarios.
- `src/logic/autenticacion.py`: hash y verificación de contraseñas, autenticación, límites de intentos y configuración inicial.
- `src/logic/productos.py`: operaciones de inventario.
- `src/logic/usuarios.py`: operaciones de administración de cuentas y validación del rol administrador.
- `src/data/conectar.py`: conexión SQLite y creación de tablas.
- `tests/test_autenticacion.py`: pruebas de hash, migración de contraseñas y bloqueo de intentos.

### Base de datos

Al ejecutar desde Python, la base de datos se guarda en `src/data/inventario.db`, independientemente del directorio de trabajo. En un ejecutable PyInstaller se usa el directorio de datos del usuario:

- Windows: `%LOCALAPPDATA%\TalentoTech\inventario.db`
- macOS: `~/Library/Application Support/TalentoTech/inventario.db`
- Linux: `$XDG_DATA_HOME/TalentoTech/inventario.db` o, si no está definido, `~/.local/share/TalentoTech/inventario.db`

Al conectarse, el programa crea las tablas si no existen. `intentos_login` guarda los bloqueos temporales. En sistemas POSIX, la aplicación restringe los permisos del directorio y el archivo de la base de datos; en Windows, el archivo queda bajo el directorio de datos del usuario.

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
| `contrasena` | Hash scrypt; algunas cuentas antiguas pueden conservar texto plano hasta migrarse |
| `rol`        | `Admin` o `Usuario` |

### Seguridad y migración de datos

- Las contraseñas se derivan con scrypt y una sal aleatoria. No se almacenan ni se comparan como texto plano para las cuentas nuevas.
- En las bases existentes, las contraseñas antiguas se convierten a hash después de un inicio de sesión correcto. La cuenta inicial conocida de versiones anteriores debe reemplazar su contraseña antes de iniciar sesión.
- El bloqueo se aplica al nombre de usuario (también si no existe) después de cinco intentos fallidos y dura un minuto. Se guarda en SQLite, por lo que sobrevive al cierre de la aplicación.
- Las bases de datos pueden contener información personal y están excluidas del control de versiones. Si ya se compartió una base, quitarla de un commit no la elimina del historial de Git ni de las copias existentes: coordina la limpieza del historial y cambia cualquier credencial expuesta.
- Esta aplicación local no protege contra alguien con acceso al equipo, al código o al archivo SQLite; los roles son controles dentro de la aplicación, no una frontera de seguridad del sistema operativo. Para uso compartido o información sensible, utiliza un servicio central con autorización del lado servidor y protege la base y sus copias de seguridad mediante permisos del sistema operativo.

### Generar un ejecutable

Desde la raíz del proyecto:

```bash
pyinstaller --onefile main.py
```

PyInstaller genera el ejecutable en `dist/`. La base de datos no se incluye en el ejecutable; al iniciarlo, se crea en el directorio de datos del usuario descrito arriba. Si vienes de una versión anterior ejecutable que guardaba la base en otra ubicación, copia la base de datos existente a la nueva ubicación para conservar los datos y aplicar la migración de contraseñas.

## Tecnologías

- Python
- SQLite (`sqlite3`)
- Colorama
- PyInstaller (opcional)

## Autor

Gregory Rodriguez
