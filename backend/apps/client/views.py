from rest_framework.permissions import AllowAny, IsAuthenticated
from apps.security.permissions import HasResourceAccess
from rest_framework import viewsets

from apps.client.models import Client
from apps.client.serializers import ClientSerializer
from apps.common.status import RecordStatus


class ClientViewSet(viewsets.ModelViewSet):
    """CRUD homogéneo de clientes para TazaNorte con soporte de baja lógica."""
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
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
