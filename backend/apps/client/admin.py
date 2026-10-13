from django.contrib import admin
from apps.client.models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email",
        "phone",
        "status",
        "created_at",
    )
    list_filter = ("status",)
    search_fields = ("name", "email", "phone")
    list_editable = ("status",)
    ordering = ("name", "id")
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (
            "Información del Cliente",
            {"fields": ("name", "email", "phone")},
        ),
        ("Estado", {"fields": ("status",)}),
        (
            "Auditoría",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )
