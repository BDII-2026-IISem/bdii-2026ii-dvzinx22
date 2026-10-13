from django.core.exceptions import ImproperlyConfigured
from django.test import SimpleTestCase, TestCase
from django.contrib.auth import authenticate, get_user_model
from config.database import database_from_environ
from apps.common.status import RecordStatus

User = get_user_model()


class DatabaseSelectionTests(SimpleTestCase):
    def _env(self, engine):
        return {
            "DB_ENGINE": engine,
            "POSTGRES_DB": "storelab",
            "POSTGRES_USER": "storelab",
            "POSTGRES_PASSWORD": "storelab",
            "POSTGRES_HOST": "127.0.0.1",
            "POSTGRES_PORT": "5432",
            "MYSQL_DB": "storelab",
            "MYSQL_USER": "storelab",
            "MYSQL_PASSWORD": "storelab",
            "MYSQL_HOST": "127.0.0.1",
            "MYSQL_PORT": "3306",
            "MSSQL_DB": "storelab",
            "MSSQL_USER": "storelab",
            "MSSQL_PASSWORD": "storelab",
            "MSSQL_HOST": "127.0.0.1",
            "MSSQL_PORT": "1433",
            "ORACLE_DB": "storelab",
            "ORACLE_USER": "storelab",
            "ORACLE_PASSWORD": "storelab",
            "ORACLE_HOST": "127.0.0.1",
            "ORACLE_PORT": "1521",
            "ORACLE_SERVICE_NAME": "FREEPDB1",
        }

    def test_postgresql_engine(self):
        config = database_from_environ(self._env("postgresql"))
        self.assertEqual(config["default"]["ENGINE"], "django.db.backends.postgresql")

    def test_mysql_engine(self):
        config = database_from_environ(self._env("mysql"))
        self.assertEqual(config["default"]["ENGINE"], "django.db.backends.mysql")
        self.assertEqual(config["default"]["OPTIONS"]["charset"], "utf8mb4")

    def test_mssql_engine(self):
        config = database_from_environ(self._env("mssql"))
        self.assertEqual(config["default"]["ENGINE"], "mssql")

    def test_oracle_uses_service_name(self):
        config = database_from_environ(self._env("oracle"))
        self.assertIn("SERVICE_NAME=FREEPDB1", config["default"]["NAME"])
        self.assertEqual(config["default"]["PORT"], "")

    def test_invalid_engine(self):
        with self.assertRaises(ImproperlyConfigured):
            database_from_environ({"DB_ENGINE": "sqlite"})

    def test_missing_variable(self):
        env = self._env("postgresql")
        env["POSTGRES_DB"] = ""
        with self.assertRaises(ImproperlyConfigured):
            database_from_environ(env)


class AuthFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="TestUser@Example.COM",
            password="securepassword123",
        )

    def test_user_creation_defaults_inactive(self):
        self.assertEqual(self.user.status, RecordStatus.INACTIVE)
        self.assertFalse(self.user.is_active)
        self.assertEqual(self.user.email, "testuser@example.com")

    def test_user_password_verification(self):
        self.assertTrue(self.user.check_password("securepassword123"))
        self.assertFalse(self.user.check_password("wrongpassword"))

    def test_inactive_user_cannot_authenticate(self):
        user = authenticate(username="testuser", password="securepassword123")
        self.assertIsNone(user)

    def test_active_user_authentication_by_username(self):
        self.user.status = RecordStatus.ACTIVE
        self.user.save()
        user = authenticate(username="testuser", password="securepassword123")
        self.assertIsNotNone(user)
        self.assertEqual(user.username, "testuser")

    def test_superuser_is_active(self):
        admin = User.objects.create_superuser(
            username="adminuser",
            email="admin@example.com",
            password="adminpassword123",
        )
        self.assertEqual(admin.status, RecordStatus.ACTIVE)
        self.assertTrue(admin.is_active)
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)
