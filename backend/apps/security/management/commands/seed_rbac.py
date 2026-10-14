from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.urls import resolve

from apps.common.status import RecordStatus
from apps.security.models import Resource, ResourceRole, Role, RoleUser

User = get_user_model()

SAMPLES = [
    # clients (6)
    ("GET", "/api/clients/"),
    ("POST", "/api/clients/"),
    ("GET", "/api/clients/1/"),
    ("PUT", "/api/clients/1/"),
    ("PATCH", "/api/clients/1/"),
    ("DELETE", "/api/clients/1/"),

    # product-types (6)
    ("GET", "/api/product-types/"),
    ("POST", "/api/product-types/"),
    ("GET", "/api/product-types/1/"),
    ("PUT", "/api/product-types/1/"),
    ("PATCH", "/api/product-types/1/"),
    ("DELETE", "/api/product-types/1/"),

    # products (6)
    ("GET", "/api/products/"),
    ("POST", "/api/products/"),
    ("GET", "/api/products/1/"),
    ("PUT", "/api/products/1/"),
    ("PATCH", "/api/products/1/"),
    ("DELETE", "/api/products/1/"),

    # products/available (1)
    ("GET", "/api/products/available/"),

    # sales (4)
    ("GET", "/api/sales/"),
    ("POST", "/api/sales/"),
    ("GET", "/api/sales/1/"),
    ("DELETE", "/api/sales/1/"),

    # users (6)
    ("GET", "/api/users/"),
    ("POST", "/api/users/"),
    ("GET", "/api/users/1/"),
    ("PUT", "/api/users/1/"),
    ("PATCH", "/api/users/1/"),
    ("DELETE", "/api/users/1/"),

    # roles (6)
    ("GET", "/api/roles/"),
    ("POST", "/api/roles/"),
    ("GET", "/api/roles/1/"),
    ("PUT", "/api/roles/1/"),
    ("PATCH", "/api/roles/1/"),
    ("DELETE", "/api/roles/1/"),

    # role-users (6)
    ("GET", "/api/role-users/"),
    ("POST", "/api/role-users/"),
    ("GET", "/api/role-users/1/"),
    ("PUT", "/api/role-users/1/"),
    ("PATCH", "/api/role-users/1/"),
    ("DELETE", "/api/role-users/1/"),

    # resources (6)
    ("GET", "/api/resources/"),
    ("POST", "/api/resources/"),
    ("GET", "/api/resources/1/"),
    ("PUT", "/api/resources/1/"),
    ("PATCH", "/api/resources/1/"),
    ("DELETE", "/api/resources/1/"),

    # resource-roles (6)
    ("GET", "/api/resource-roles/"),
    ("POST", "/api/resource-roles/"),
    ("GET", "/api/resource-roles/1/"),
    ("PUT", "/api/resource-roles/1/"),
    ("PATCH", "/api/resource-roles/1/"),
    ("DELETE", "/api/resource-roles/1/"),
]


class Command(BaseCommand):
    help = "Sincroniza los recursos RBAC a partir de las rutas reales y concede el rol admin."

    def add_arguments(self, parser):
        parser.add_argument(
            "--username",
            type=str,
            default=None,
            help="Nombre de usuario al que se le asignará el rol admin.",
        )

    def handle(self, *args, **options):
        username = options.get("username")

        # 1. Crear o reactivar el rol admin
        admin_role, _created = Role.objects.get_or_create(
            name="admin",
            defaults={
                "description": "Rol de administración con acceso total al sistema",
                "status": RecordStatus.ACTIVE,
            },
        )
        if not _created and admin_role.status != RecordStatus.ACTIVE:
            admin_role.status = RecordStatus.ACTIVE
            admin_role.save(update_fields=["status"])

        # 2. Recorrer muestras y resolver rutas
        seen_routes = set()
        for method, sample_path in SAMPLES:
            match = resolve(sample_path)
            route = match.route
            method_upper = method.upper()

            if (method_upper, route) in seen_routes:
                continue
            seen_routes.add((method_upper, route))

            resource, _res_created = Resource.objects.get_or_create(
                method=method_upper,
                route=route,
                defaults={
                    "name": f"{method_upper} {route}",
                    "status": RecordStatus.ACTIVE,
                },
            )
            if not _res_created and resource.status != RecordStatus.ACTIVE:
                resource.status = RecordStatus.ACTIVE
                resource.save(update_fields=["status"])

            grant, _grant_created = ResourceRole.objects.get_or_create(
                resource=resource,
                role=admin_role,
                defaults={"status": RecordStatus.ACTIVE},
            )
            if not _grant_created and grant.status != RecordStatus.ACTIVE:
                grant.status = RecordStatus.ACTIVE
                grant.save(update_fields=["status"])

        # 3. Asignar rol admin al usuario si se especifica
        if username:
            try:
                user = User.objects.get(username=username)
                ru, _ru_created = RoleUser.objects.get_or_create(
                    role=admin_role,
                    user=user,
                    defaults={"status": RecordStatus.ACTIVE},
                )
                if not _ru_created and ru.status != RecordStatus.ACTIVE:
                    ru.status = RecordStatus.ACTIVE
                    ru.save(update_fields=["status"])
            except User.DoesNotExist:
                self.stderr.write(self.style.WARNING(f"Usuario '{username}' no encontrado."))

        self.stdout.write(self.style.SUCCESS("Recursos RBAC sincronizados."))

