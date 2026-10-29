from rest_framework.permissions import AllowAny, IsAuthenticated
from apps.security.permissions import HasResourceAccess
from rest_framework import viewsets
from rest_framework.generics import ListAPIView

from apps.common.status import RecordStatus
from apps.product.models import Product, ProductType
from apps.product.serializers import ProductSerializer, ProductTypeSerializer


class CatalogViewSet(viewsets.ModelViewSet):
    """ViewSet base para el catálogo de TazaNorte con baja lógica y filtro por estado."""
    permission_classes = [AllowAny]
    lookup_value_converter = "int"

    def get_queryset(self):
        queryset = super().get_queryset()
        status_value = self.request.query_params.get("status")
        if status_value:
            queryset = queryset.filter(status=status_value)
        return queryset

    def perform_destroy(self, instance):
        instance.status = RecordStatus.INACTIVE
        instance.save(update_fields=["status", "updated_at"])


class ProductTypeViewSet(CatalogViewSet):
    """CRUD de categorías de menú en TazaNorte."""
    queryset = ProductType.objects.all()
    serializer_class = ProductTypeSerializer


class ProductViewSet(CatalogViewSet):
    """CRUD de productos de cafetería en TazaNorte con carga ansiosa de categoría."""
    queryset = Product.objects.select_related("product_type")
    serializer_class = ProductSerializer


class AvailableProductListAPIView(ListAPIView):
    """Lista de productos activos con categoría activa para la venta en TazaNorte."""
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.select_related("product_type").filter(
            status=RecordStatus.ACTIVE,
            product_type__status=RecordStatus.ACTIVE,
        )
