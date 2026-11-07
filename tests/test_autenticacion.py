import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from src.logic import autenticacion


class AutenticacionTests(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.database_path = Path(self.temporary_directory.name) / "inventario.db"
        self.database_path_patch = patch.object(
            autenticacion.db, "DB_PATH", self.database_path
        )
        self.database_path_patch.start()

    def tearDown(self):
        self.database_path_patch.stop()
        self.temporary_directory.cleanup()

    def test_password_hash_is_salted_and_verified(self):
        first_hash = autenticacion.hash_password("una contraseña segura")
        second_hash = autenticacion.hash_password("una contraseña segura")

        self.assertNotEqual(first_hash, second_hash)
        self.assertTrue(
            autenticacion.verify_password("una contraseña segura", first_hash)
        )
        self.assertFalse(autenticacion.verify_password("incorrecta", first_hash))

    def test_initial_admin_is_created_with_a_hash(self):
        autenticacion.crear_administrador_inicial(
            "admin", "Apellido", "admin@example.com", "una contraseña segura"
        )

        conexion = autenticacion.db.conectar()
        stored_password = conexion.execute(
            "SELECT contrasena FROM usuarios WHERE nombre = 'admin'"
        ).fetchone()[0]
        conexion.close()

        self.assertTrue(stored_password.startswith("scrypt$"))
        self.assertEqual(
            autenticacion.autenticar("admin", "una contraseña segura"),
            (True, "Admin", False),
        )

    def test_legacy_password_is_upgraded_after_successful_login(self):
        conexion = autenticacion.db.conectar()
        conexion.execute(
            "INSERT INTO usuarios (nombre, apellido, email, contrasena, rol) "
            "VALUES (?, ?, ?, ?, ?)",
            ("legacy", "Apellido", "legacy@example.com", "plain old secret", "Usuario"),
        )
        conexion.commit()
        conexion.close()

        self.assertEqual(
            autenticacion.autenticar("legacy", "plain old secret"),
            (True, "Usuario", False),
        )
        conexion = autenticacion.db.conectar()
        stored_password = conexion.execute(
            "SELECT contrasena FROM usuarios WHERE nombre = 'legacy'"
        ).fetchone()[0]
        conexion.close()
        self.assertTrue(stored_password.startswith("scrypt$"))

    def test_known_legacy_admin_must_replace_its_password(self):
        conexion = autenticacion.db.conectar()
        conexion.execute(
            "INSERT INTO usuarios (nombre, apellido, email, contrasena, rol) "
            "VALUES (?, ?, ?, ?, ?)",
            (
                "Admin",
                "Admin",
                "glrd4726@gmail.com",
                "Admin",
                "Admin",
            ),
        )
        conexion.commit()
        conexion.close()

        self.assertTrue(autenticacion.hay_administrador_legacy())
        autenticacion.reemplazar_contrasena_admin_legacy("otra contraseña segura")
        self.assertFalse(autenticacion.hay_administrador_legacy())
        self.assertEqual(
            autenticacion.autenticar("Admin", "Admin"),
            (False, None, False),
        )
        self.assertEqual(
            autenticacion.autenticar("Admin", "otra contraseña segura"),
            (True, "Admin", False),
        )

    def test_failed_attempts_persistently_lock_username(self):
        for _ in range(5):
            authenticated, _, _ = autenticacion.autenticar("admin", "wrong")
            self.assertFalse(authenticated)

        self.assertEqual(
            autenticacion.autenticar("admin", "correct"),
            (False, None, True),
        )

        conexion = autenticacion.db.conectar()
        attempt = conexion.execute(
            "SELECT intentos, bloqueado_hasta FROM intentos_login "
            "WHERE nombre_usuario = 'admin'"
        ).fetchone()
        conexion.close()
        self.assertEqual(attempt[0], 5)
        self.assertGreater(attempt[1], 0)


if __name__ == "__main__":
    unittest.main()
