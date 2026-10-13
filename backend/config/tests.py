from django.test import SimpleTestCase
from django.core.exceptions import ImproperlyConfigured
from config.database import database_from_environ


class DatabaseSelectionTests(SimpleTestCase):
    def test_postgresql_engine(self):
        env = {
            "DB_ENGINE": "postgresql",
            "POSTGRES_DB": "test_db",
            "POSTGRES_USER": "test_user",
            "POSTGRES_PASSWORD": "secret_password",
            "POSTGRES_HOST": "127.0.0.1",
            "POSTGRES_PORT": "5432",
        }
        db = database_from_environ(env)["default"]
        self.assertEqual(db["ENGINE"], "django.db.backends.postgresql")

    def test_mysql_engine(self):
        env = {
            "DB_ENGINE": "mysql",
            "MYSQL_DB": "test_db",
            "MYSQL_USER": "test_user",
            "MYSQL_PASSWORD": "secret_password",
            "MYSQL_HOST": "127.0.0.1",
            "MYSQL_PORT": "3306",
        }
        db = database_from_environ(env)["default"]
        self.assertEqual(db["ENGINE"], "django.db.backends.mysql")

    def test_mssql_engine(self):
        env = {
            "DB_ENGINE": "mssql",
            "MSSQL_DB": "test_db",
            "MSSQL_USER": "test_user",
            "MSSQL_PASSWORD": "secret_password",
            "MSSQL_HOST": "127.0.0.1",
            "MSSQL_PORT": "1433",
        }
        db = database_from_environ(env)["default"]
        self.assertEqual(db["ENGINE"], "mssql")

    def test_oracle_engine_and_dsn(self):
        env = {
            "DB_ENGINE": "oracle",
            "ORACLE_DB": "test_db",
            "ORACLE_USER": "test_user",
            "ORACLE_PASSWORD": "secret_password",
            "ORACLE_HOST": "127.0.0.1",
            "ORACLE_PORT": "1521",
            "ORACLE_SERVICE_NAME": "XEPDB1",
        }
        db = database_from_environ(env)["default"]
        self.assertEqual(db["ENGINE"], "django.db.backends.oracle")
        self.assertIn("SERVICE_NAME=XEPDB1", db["NAME"])

    def test_invalid_engine_raises_improperly_configured(self):
        env = {"DB_ENGINE": "sqlite"}
        with self.assertRaises(ImproperlyConfigured):
            database_from_environ(env)

    def test_missing_required_variable_raises(self):
        env = {"DB_ENGINE": "postgresql"}
        with self.assertRaises(ImproperlyConfigured):
            database_from_environ(env)
