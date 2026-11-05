from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from apps.security.models import User, Role, RoleUser, Resource, ResourceRole


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("username", "email", "first_name", "last_name", "status", "is_staff")
    list_filter = ("status", "is_staff", "is_superuser")
    list_editable = ("status",)
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Auditoría y Estado", {"fields": ("status",)}),
    )


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "status", "created_at")
    list_filter = ("status",)
    list_editable = ("status",)
    search_fields = ("name", "description")


@admin.register(RoleUser)
class RoleUserAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "role", "status", "created_at")
    list_filter = ("status", "role")
    list_editable = ("status",)
    search_fields = ("user__username", "role__name")


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ("id", "method", "route", "name", "status")
    list_filter = ("status", "method")
    list_editable = ("status",)
    search_fields = ("route", "name")


@admin.register(ResourceRole)
class ResourceRoleAdmin(admin.ModelAdmin):
    list_display = ("id", "role", "resource", "status", "created_at")
    list_filter = ("status", "role", "resource__method")
    list_editable = ("status",)
    search_fields = ("role__name", "resource__route", "resource__name")
