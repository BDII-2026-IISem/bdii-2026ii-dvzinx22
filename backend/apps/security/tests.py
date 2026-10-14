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


class UserAuthModelTests(TestCase):
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


from datetime import timedelta
from django.utils import timezone
from apps.security.models import RefreshToken
from apps.security.tokens import generate_refresh_value, hash_token


class RefreshTokenModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="barista",
            email="barista@tazanorte.com",
            password="securepassword123",
        )
        self.user.status = RecordStatus.ACTIVE
        self.user.save()

    def test_token_generation_and_hashing(self):
        raw_token = generate_refresh_value()
        self.assertTrue(len(raw_token) >= 48)
        hashed = hash_token(raw_token)
        self.assertEqual(len(hashed), 64)
        self.assertNotEqual(raw_token, hashed)
        self.assertEqual(hashed, hash_token(raw_token))

    def test_refresh_token_creation_defaults(self):
        raw_token = generate_refresh_value()
        token_hash = hash_token(raw_token)
        refresh = RefreshToken.objects.create(
            user=self.user,
            token_hash=token_hash,
            expires_at=RefreshToken.default_expiry(),
        )
        self.assertEqual(refresh.status, RecordStatus.ACTIVE)
        self.assertIsNotNone(refresh.family_id)
        self.assertIsNone(refresh.revoked_at)
        self.assertIsNone(refresh.replaced_by)
        self.assertTrue(refresh.is_usable)

    def test_refresh_token_revoked_is_not_usable(self):
        refresh = RefreshToken.objects.create(
            user=self.user,
            token_hash=hash_token(generate_refresh_value()),
            expires_at=RefreshToken.default_expiry(),
            revoked_at=timezone.now(),
        )
        self.assertFalse(refresh.is_usable)

    def test_refresh_token_expired_is_not_usable(self):
        refresh = RefreshToken.objects.create(
            user=self.user,
            token_hash=hash_token(generate_refresh_value()),
            expires_at=timezone.now() - timedelta(minutes=5),
        )
        self.assertFalse(refresh.is_usable)

    def test_refresh_token_replaced_is_not_usable(self):
        refresh_1 = RefreshToken.objects.create(
            user=self.user,
            token_hash=hash_token(generate_refresh_value()),
            expires_at=RefreshToken.default_expiry(),
        )
        refresh_2 = RefreshToken.objects.create(
            user=self.user,
            token_hash=hash_token(generate_refresh_value()),
            expires_at=RefreshToken.default_expiry(),
        )
        refresh_1.replaced_by = refresh_2
        refresh_1.save()
        self.assertFalse(refresh_1.is_usable)
        self.assertTrue(refresh_2.is_usable)

    def test_refresh_token_inactive_status_is_not_usable(self):
        refresh = RefreshToken.objects.create(
            user=self.user,
            token_hash=hash_token(generate_refresh_value()),
            expires_at=RefreshToken.default_expiry(),
            status=RecordStatus.INACTIVE,
        )
        self.assertFalse(refresh.is_usable)


from django.db import IntegrityError
from apps.security.models import Role, RoleUser, Resource, ResourceRole, HttpMethod


class RbacModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="cajero",
            email="cajero@tazanorte.com",
            password="cajeropassword123",
        )
        self.role = Role.objects.create(
            name="Cajero",
            description="Rol de atención y registro de ventas",
        )
        self.resource = Resource.objects.create(
            name="Venta Register",
            method=HttpMethod.POST,
            route="api/sales/",
        )

    def test_role_defaults_and_str(self):
        self.assertEqual(self.role.status, RecordStatus.INACTIVE)
        self.assertEqual(str(self.role), "Cajero")

    def test_role_unique_name(self):
        with self.assertRaises(IntegrityError):
            Role.objects.create(name="Cajero")

    def test_role_user_assignment_and_uniqueness(self):
        ru = RoleUser.objects.create(role=self.role, user=self.user)
        self.assertEqual(ru.status, RecordStatus.INACTIVE)
        with self.assertRaises(IntegrityError):
            RoleUser.objects.create(role=self.role, user=self.user)

    def test_resource_defaults_and_uniqueness(self):
        self.assertEqual(self.resource.status, RecordStatus.INACTIVE)
        self.assertEqual(str(self.resource), "POST api/sales/")
        with self.assertRaises(IntegrityError):
            Resource.objects.create(
                name="Venta Register Duplicate",
                method=HttpMethod.POST,
                route="api/sales/",
            )

    def test_resource_role_grant_and_uniqueness(self):
        rr = ResourceRole.objects.create(resource=self.resource, role=self.role)
        self.assertEqual(rr.status, RecordStatus.INACTIVE)
        with self.assertRaises(IntegrityError):
            ResourceRole.objects.create(resource=self.resource, role=self.role)


from rest_framework import status
from rest_framework.test import APITestCase
from apps.common.testing import PASSWORD, create_active_user


class AuthFlowTests(APITestCase):
    def setUp(self):
        self.user = create_active_user()

    def test_login_with_username_and_email(self):
        by_username = self.client.post(
            "/api/auth/login/",
            {"username": "ana", "password": PASSWORD},
            format="json",
        )
        self.assertEqual(by_username.status_code, status.HTTP_200_OK)
        self.assertIn("access", by_username.data)
        self.assertIn("refresh", by_username.data)
        self.assertNotIn("password", by_username.data)
        stored = RefreshToken.objects.get(user=self.user)
        self.assertEqual(stored.token_hash, hash_token(by_username.data["refresh"]))

        by_email = self.client.post(
            "/api/auth/login/",
            {"email": "ANA@tazanorte.test", "password": PASSWORD},
            format="json",
        )
        self.assertEqual(by_email.status_code, status.HTTP_200_OK)

    def test_inactive_user_and_bad_password_are_401(self):
        self.user.status = RecordStatus.INACTIVE
        self.user.save()
        inactive = self.client.post(
            "/api/auth/login/",
            {"username": "ana", "password": PASSWORD},
            format="json",
        )
        self.assertEqual(inactive.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(inactive.data.get("detail"), "Credenciales inválidas.")

        # Test bad password
        self.user.status = RecordStatus.ACTIVE
        self.user.save()
        bad_pw = self.client.post(
            "/api/auth/login/",
            {"username": "ana", "password": "wrongpassword999"},
            format="json",
        )
        self.assertEqual(bad_pw.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(bad_pw.data.get("detail"), "Credenciales inválidas.")
