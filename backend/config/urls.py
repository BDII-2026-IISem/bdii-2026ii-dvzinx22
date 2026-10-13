"""
Configuración de URLs globales del proyecto TazaNorte.
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("apps.client.urls")),
    path("api/", include("apps.product.urls")),
]
