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
from apps.common.testing import PASSWORD, create_active_user, grant, grant_crud


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

    def test_refresh_rotates_and_reuse_revokes_family(self):
        login = self.client.post(
            "/api/auth/login/",
            {"username": "ana", "password": PASSWORD},
            format="json",
        )
        first = login.data["refresh"]
        rotated = self.client.post("/api/auth/refresh/", {"refresh": first}, format="json")
        self.assertEqual(rotated.status_code, status.HTTP_200_OK)
        second = rotated.data["refresh"]
        self.assertNotEqual(first, second)
        reused = self.client.post("/api/auth/refresh/", {"refresh": first}, format="json")
        self.assertEqual(reused.status_code, status.HTTP_401_UNAUTHORIZED)
        after_reuse = self.client.post("/api/auth/refresh/", {"refresh": second}, format="json")
        self.assertEqual(after_reuse.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout_invalidates_refresh(self):
        login = self.client.post(
            "/api/auth/login/",
            {"username": "ana", "password": PASSWORD},
            format="json",
        )
        raw = login.data["refresh"]
        logout = self.client.post("/api/auth/logout/", {"refresh": raw}, format="json")
        self.assertEqual(logout.status_code, status.HTTP_204_NO_CONTENT)
        again = self.client.post("/api/auth/refresh/", {"refresh": raw}, format="json")
        self.assertEqual(again.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_profile_requires_token_and_rejects_inactive_user(self):
        anonymous = self.client.get("/api/auth/profile/")
        self.assertEqual(anonymous.status_code, status.HTTP_401_UNAUTHORIZED)
        login = self.client.post(
            "/api/auth/login/",
            {"username": "ana", "password": PASSWORD},
            format="json",
        )
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {login.data['access']}")
        profile = self.client.get("/api/auth/profile/")
        self.assertEqual(profile.status_code, status.HTTP_200_OK)
        self.assertEqual(profile.data["username"], "ana")
        patched = self.client.patch(
            "/api/auth/profile/",
            {"firstName": "Ana"},
            format="json",
        )
        self.assertEqual(patched.status_code, status.HTTP_200_OK)
        self.user.status = RecordStatus.INACTIVE
        self.user.save()
        denied = self.client.get("/api/auth/profile/")
        self.assertEqual(denied.status_code, status.HTTP_401_UNAUTHORIZED)


from unittest.mock import MagicMock
from apps.security.permissions import HasResourceAccess


class HasResourceAccessPermissionTests(TestCase):
    def setUp(self):
        self.permission = HasResourceAccess()
        self.user = User.objects.create_user(
            username="barista_rbac",
            email="barista_rbac@tazanorte.com",
            password="securepassword123",
            status=RecordStatus.ACTIVE,
        )
        self.role = Role.objects.create(
            name="Barista",
            status=RecordStatus.ACTIVE,
        )
        self.resource = Resource.objects.create(
            name="Available Products",
            method=HttpMethod.GET,
            route="api/products/available/",
            status=RecordStatus.ACTIVE,
        )
        self.role_user = RoleUser.objects.create(
            role=self.role,
            user=self.user,
            status=RecordStatus.ACTIVE,
        )
        self.resource_role = ResourceRole.objects.create(
            resource=self.resource,
            role=self.role,
            status=RecordStatus.ACTIVE,
        )

    def _mock_request(self, user, method="GET", route="api/products/available/"):
        request = MagicMock()
        request.user = user
        request.method = method
        match = MagicMock()
        match.route = route
        request.resolver_match = match
        return request

    def test_anonymous_user_is_denied(self):
        anon = MagicMock()
        anon.is_authenticated = False
        request = self._mock_request(anon)
        self.assertFalse(self.permission.has_permission(request, None))

    def test_inactive_user_is_denied(self):
        self.user.status = RecordStatus.INACTIVE
        self.user.save()
        request = self._mock_request(self.user)
        self.assertFalse(self.permission.has_permission(request, None))

    def test_options_method_is_allowed_for_active_user(self):
        request = self._mock_request(self.user, method="OPTIONS")
        self.assertTrue(self.permission.has_permission(request, None))

    def test_active_grant_chain_is_allowed(self):
        request = self._mock_request(self.user, method="GET", route="api/products/available/")
        self.assertTrue(self.permission.has_permission(request, None))

    def test_head_method_evaluates_as_get(self):
        request = self._mock_request(self.user, method="HEAD", route="api/products/available/")
        self.assertTrue(self.permission.has_permission(request, None))

    def test_inactive_role_denies_permission(self):
        self.role.status = RecordStatus.INACTIVE
        self.role.save()
        request = self._mock_request(self.user)
        self.assertFalse(self.permission.has_permission(request, None))

    def test_inactive_role_user_denies_permission(self):
        self.role_user.status = RecordStatus.INACTIVE
        self.role_user.save()
        request = self._mock_request(self.user)
        self.assertFalse(self.permission.has_permission(request, None))

    def test_inactive_resource_role_denies_permission(self):
        self.resource_role.status = RecordStatus.INACTIVE
        self.resource_role.save()
        request = self._mock_request(self.user)
        self.assertFalse(self.permission.has_permission(request, None))

    def test_inactive_resource_denies_permission(self):
        self.resource.status = RecordStatus.INACTIVE
        self.resource.save()
        request = self._mock_request(self.user)
        self.assertFalse(self.permission.has_permission(request, None))


class SecurityMatrixApiTests(APITestCase):
    def setUp(self):
        self.admin_user = create_active_user(username="admin_matrix", email="admin_matrix@tazanorte.test")
        grant_crud(self.admin_user, "/api/users/", "/api/users/1/")
        grant_crud(self.admin_user, "/api/roles/", "/api/roles/1/")
        grant_crud(self.admin_user, "/api/role-users/", "/api/role-users/1/")
        grant_crud(self.admin_user, "/api/resources/", "/api/resources/1/")
        grant_crud(self.admin_user, "/api/resource-roles/", "/api/resource-roles/1/")
        self.client.force_authenticate(user=self.admin_user)

    def test_role_crud(self):
        """CRUD de rol: POST, GET lista, GET detalle, PATCH y DELETE con baja lógica."""
        created = self.client.post(
            "/api/roles/",
            {"name": "Supervisor", "description": "Control de turnos de cafetería"},
            format="json",
        )
        self.assertEqual(created.status_code, status.HTTP_201_CREATED)
        pk = created.data["id"]

        list_resp = self.client.get("/api/roles/")
        self.assertEqual(list_resp.status_code, status.HTTP_200_OK)

        detail_resp = self.client.get(f"/api/roles/{pk}/")
        self.assertEqual(detail_resp.status_code, status.HTTP_200_OK)
        self.assertEqual(detail_resp.data["name"], "Supervisor")

        patched = self.client.patch(
            f"/api/roles/{pk}/",
            {"description": "Supervisor general"},
            format="json",
        )
        self.assertEqual(patched.status_code, status.HTTP_200_OK)

        deleted = self.client.delete(f"/api/roles/{pk}/")
        self.assertEqual(deleted.status_code, status.HTTP_204_NO_CONTENT)

        # Verificar baja lógica: la fila persiste inactiva
        role_db = Role.objects.get(pk=pk)
        self.assertEqual(role_db.status, RecordStatus.INACTIVE)

    def test_user_role_resource_chain(self):
        """
        Construcción granular de la cadena RBAC para un nuevo usuario:
        1. Crea rol 'bodega' activo.
        2. Crea usuario 'bodega1' activo.
        3. 'bodega1' entra a GET /api/clients/ -> 403 (sin rol).
        4. Asigna RoleUser 'bodega' a 'bodega1' -> 403 (falta recurso).
        5. Crea recurso 'GET api/clients/' -> 403 (falta ResourceRole).
        6. Asigna ResourceRole -> GET /api/clients/ responde 200 OK.
        7. POST /api/clients/ sigue en 403 (no fue concedido).
        """
        # 1. Crear rol bodega activo
        role_resp = self.client.post(
            "/api/roles/",
            {"name": "bodega", "status": RecordStatus.ACTIVE},
            format="json",
        )
        self.assertEqual(role_resp.status_code, status.HTTP_201_CREATED)
        role_id = role_resp.data["id"]

        # 2. Crear usuario bodega1 activo
        user_resp = self.client.post(
            "/api/users/",
            {
                "username": "bodega1",
                "email": "bodega1@tazanorte.test",
                "password": PASSWORD,
                "status": RecordStatus.ACTIVE,
            },
            format="json",
        )
        self.assertEqual(user_resp.status_code, status.HTTP_201_CREATED)
        self.assertNotIn("password", user_resp.data)
        user_id = user_resp.data["id"]
        bodega_user = User.objects.get(pk=user_id)

        # 3. Intentar como bodega1 sin asignación
        self.client.force_authenticate(user=bodega_user)
        self.assertEqual(self.client.get("/api/clients/").status_code, status.HTTP_403_FORBIDDEN)

        # 4. Asignar rol a bodega1
        self.client.force_authenticate(user=self.admin_user)
        ru_resp = self.client.post(
            "/api/role-users/",
            {"role": role_id, "user": user_id, "status": RecordStatus.ACTIVE},
            format="json",
        )
        self.assertEqual(ru_resp.status_code, status.HTTP_201_CREATED)

        self.client.force_authenticate(user=bodega_user)
        self.assertEqual(self.client.get("/api/clients/").status_code, status.HTTP_403_FORBIDDEN)

        # 5. Crear recurso GET api/clients/
        self.client.force_authenticate(user=self.admin_user)
        res_resp = self.client.post(
            "/api/resources/",
            {"name": "GET Clientes", "method": "GET", "route": "api/clients/", "status": RecordStatus.ACTIVE},
            format="json",
        )
        self.assertEqual(res_resp.status_code, status.HTTP_201_CREATED)
        res_id = res_resp.data["id"]

        self.client.force_authenticate(user=bodega_user)
        self.assertEqual(self.client.get("/api/clients/").status_code, status.HTTP_403_FORBIDDEN)

        # 6. Conceder ResourceRole
        self.client.force_authenticate(user=self.admin_user)
        rr_resp = self.client.post(
            "/api/resource-roles/",
            {"role": role_id, "resource": res_id, "status": RecordStatus.ACTIVE},
            format="json",
        )
        self.assertEqual(rr_resp.status_code, status.HTTP_201_CREATED)

        # 7. Ahora bodega1 sí puede consultar clientes
        self.client.force_authenticate(user=bodega_user)
        self.assertEqual(self.client.get("/api/clients/").status_code, status.HTTP_200_OK)
        # Pero POST sigue denegado con 403
        self.assertEqual(self.client.post("/api/clients/", {"name": "Test"}, format="json").status_code, status.HTTP_403_FORBIDDEN)


class RbacTests(APITestCase):
    def setUp(self):
        self.user = create_active_user()
        self.client.force_authenticate(user=self.user)

    def test_missing_grant_is_403_and_missing_identity_is_401(self):
        denied = self.client.get("/api/clients/")
        self.assertEqual(denied.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=None)
        anonymous = self.client.get("/api/clients/")
        self.assertEqual(anonymous.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_any_inactive_link_denies(self):
        role = grant(self.user, "GET", "/api/clients/")
        allowed = self.client.get("/api/clients/")
        self.assertEqual(allowed.status_code, status.HTTP_200_OK)

        # 1. Rol inactive -> 403
        role.status = RecordStatus.INACTIVE
        role.save(update_fields=["status"])
        self.assertEqual(self.client.get("/api/clients/").status_code, status.HTTP_403_FORBIDDEN)
        role.status = RecordStatus.ACTIVE
        role.save(update_fields=["status"])

        # 2. RoleUser inactive -> 403
        ru = RoleUser.objects.get(role=role, user=self.user)
        ru.status = RecordStatus.INACTIVE
        ru.save(update_fields=["status"])
        self.assertEqual(self.client.get("/api/clients/").status_code, status.HTTP_403_FORBIDDEN)
        ru.status = RecordStatus.ACTIVE
        ru.save(update_fields=["status"])

        # 3. ResourceRole inactive -> 403
        rr = ResourceRole.objects.get(role=role)
        rr.status = RecordStatus.INACTIVE
        rr.save(update_fields=["status"])
        self.assertEqual(self.client.get("/api/clients/").status_code, status.HTTP_403_FORBIDDEN)
        rr.status = RecordStatus.ACTIVE
        rr.save(update_fields=["status"])

        # 4. Resource inactive -> 403
        resource = rr.resource
        resource.status = RecordStatus.INACTIVE
        resource.save(update_fields=["status"])
        self.assertEqual(self.client.get("/api/clients/").status_code, status.HTTP_403_FORBIDDEN)
