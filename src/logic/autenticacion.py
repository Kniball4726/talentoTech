import hashlib
import hmac
import secrets
import sqlite3
import time

import src.data.conectar as db


_SCRYPT_N = 2**14
_SCRYPT_R = 8
_SCRYPT_P = 1
_MAX_INTENTOS = 5
_DURACION_BLOQUEO = 60
_ADMIN_INICIAL = ("Admin", "glrd4726@gmail.com", "Admin")


def hash_password(password: str) -> str:
    if not isinstance(password, str):
        raise TypeError("La contraseña debe ser texto.")
    if len(password) > 1024:
        raise ValueError("La contraseña no puede superar 1024 caracteres.")
    salt = secrets.token_bytes(16)
    digest = hashlib.scrypt(
        password.encode("utf-8"),
        salt=salt,
        n=_SCRYPT_N,
        r=_SCRYPT_R,
        p=_SCRYPT_P,
        dklen=64,
    )
    return f"scrypt${salt.hex()}${digest.hex()}"


def verify_password(password: str, stored_password: str) -> bool:
    if not isinstance(password, str) or not isinstance(stored_password, str):
        return False
    if len(password) > 1024:
        return False

    if not stored_password.startswith("scrypt$"):
        return hmac.compare_digest(
            password.encode("utf-8"), stored_password.encode("utf-8")
        )

    try:
        algorithm, salt_hex, digest_hex = stored_password.split("$")
        if algorithm != "scrypt":
            return False
        salt = bytes.fromhex(salt_hex)
        expected = bytes.fromhex(digest_hex)
        if len(salt) != 16 or len(expected) != 64:
            return False
        actual = hashlib.scrypt(
            password.encode("utf-8"),
            salt=salt,
            n=_SCRYPT_N,
            r=_SCRYPT_R,
            p=_SCRYPT_P,
            dklen=64,
        )
        return hmac.compare_digest(actual, expected)
    except (ValueError, TypeError):
        return False


def _username_key(username: str) -> str:
    return username.strip().casefold()


def _validar_contrasena_nueva(password: str) -> None:
    if not isinstance(password, str) or not 12 <= len(password) <= 1024:
        raise ValueError("La contraseña debe tener entre 12 y 1024 caracteres.")


def autenticar(username: str, password: str) -> tuple[bool, str | None, bool]:
    conexion = db.conectar()
    if conexion is None:
        raise sqlite3.OperationalError("No se pudo abrir la base de datos.")

    try:
        key = _username_key(username)
        now = time.time()
        intento = conexion.execute(
            "SELECT intentos, bloqueado_hasta FROM intentos_login "
            "WHERE nombre_usuario = ?",
            (key,),
        ).fetchone()
        if intento and intento[1] > now:
            return False, None, True

        usuarios = conexion.execute(
            "SELECT id, contrasena, rol FROM usuarios WHERE nombre = ? COLLATE NOCASE",
            (username.strip(),),
        ).fetchall()
        usuario = usuarios[0] if len(usuarios) == 1 else None
        autenticado = usuario is not None and verify_password(password, usuario[1])

        if autenticado:
            if not usuario[1].startswith("scrypt$"):
                conexion.execute(
                    "UPDATE usuarios SET contrasena = ? WHERE id = ?",
                    (hash_password(password), usuario[0]),
                )
            conexion.execute(
                "DELETE FROM intentos_login WHERE nombre_usuario = ?", (key,)
            )
            conexion.commit()
            return True, usuario[2], False

        if intento and intento[1] == 0:
            intentos = intento[0] + 1
        else:
            intentos = 1
        bloqueado_hasta = now + _DURACION_BLOQUEO if intentos >= _MAX_INTENTOS else 0
        conexion.execute(
            "INSERT INTO intentos_login (nombre_usuario, intentos, bloqueado_hasta) "
            "VALUES (?, ?, ?) ON CONFLICT(nombre_usuario) DO UPDATE SET "
            "intentos = excluded.intentos, bloqueado_hasta = excluded.bloqueado_hasta",
            (key, intentos, bloqueado_hasta),
        )
        conexion.commit()
        return False, None, bloqueado_hasta > 0
    finally:
        conexion.close()


def hay_usuarios() -> bool:
    conexion = db.conectar()
    if conexion is None:
        raise sqlite3.OperationalError("No se pudo abrir la base de datos.")
    try:
        return conexion.execute("SELECT 1 FROM usuarios LIMIT 1").fetchone() is not None
    finally:
        conexion.close()


def hay_administrador_legacy() -> bool:
    conexion = db.conectar()
    if conexion is None:
        raise sqlite3.OperationalError("No se pudo abrir la base de datos.")
    try:
        return conexion.execute(
            "SELECT 1 FROM usuarios WHERE nombre = ? AND email = ? AND rol = ? "
            "AND contrasena NOT LIKE 'scrypt$%' LIMIT 1",
            _ADMIN_INICIAL,
        ).fetchone() is not None
    finally:
        conexion.close()


def crear_administrador_inicial(
    username: str, apellido: str, email: str, password: str
) -> None:
    _validar_contrasena_nueva(password)
    conexion = db.conectar()
    if conexion is None:
        raise sqlite3.OperationalError("No se pudo abrir la base de datos.")
    try:
        password_hash = hash_password(password)
        conexion.execute("BEGIN IMMEDIATE")
        if conexion.execute("SELECT 1 FROM usuarios LIMIT 1").fetchone():
            raise RuntimeError("La configuración inicial ya fue completada.")
        conexion.execute(
            "INSERT INTO usuarios (nombre, apellido, email, contrasena, rol) "
            "VALUES (?, ?, ?, ?, 'Admin')",
            (username, apellido, email, password_hash),
        )
        conexion.commit()
    finally:
        conexion.close()


def reemplazar_contrasena_admin_legacy(password: str) -> None:
    _validar_contrasena_nueva(password)
    conexion = db.conectar()
    if conexion is None:
        raise sqlite3.OperationalError("No se pudo abrir la base de datos.")
    try:
        cursor = conexion.execute(
            "UPDATE usuarios SET contrasena = ? WHERE nombre = ? AND email = ? "
            "AND rol = ? AND contrasena NOT LIKE 'scrypt$%'",
            (hash_password(password), *_ADMIN_INICIAL),
        )
        if cursor.rowcount != 1:
            raise RuntimeError("La cuenta predeterminada ya no está disponible.")
        conexion.commit()
    finally:
        conexion.close()
