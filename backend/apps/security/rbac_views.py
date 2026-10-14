from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

from apps.security.serializers import ProfileSerializer


class ProfileAPIView(RetrieveUpdateAPIView):
    """
    Endpoint del perfil propio de usuario en TazaNorte (/api/auth/profile/).
    Requiere autenticación JWT válida sin consultar todavía matriz RBAC.
    """
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "patch", "head", "options"]

    @extend_schema(
        description="Consulta los datos de perfil del usuario autenticado vía JWT.",
        tags=["auth"],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        description="Actualiza parcialmente el perfil del usuario autenticado (nombres/apellidos).",
        tags=["auth"],
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    def get_object(self):
        return self.request.user

from rest_framework import viewsets
from apps.common.status import RecordStatus
from apps.security.permissions import HasResourceAccess
from apps.security.models import User, Role, RoleUser, Resource, ResourceRole
from apps.security.serializers import (
    UserSerializer,
    RoleSerializer,
    RoleUserSerializer,
    ResourceSerializer,
    ResourceRoleSerializer,
)


class SoftDeleteModelViewSet(viewsets.ModelViewSet):
    """
    ViewSet base para la matriz de autorización con soporte de baja lógica.
    """
    permission_classes = [IsAuthenticated, HasResourceAccess]

    def perform_destroy(self, instance):
        instance.status = RecordStatus.INACTIVE
        instance.save(update_fields=["status", "updated_at"])

    def get_queryset(self):
        status_filter = self.request.query_params.get("status")
        if status_filter:
            return self.queryset.filter(status=status_filter)
        return self.queryset.all()


class UserViewSet(SoftDeleteModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RoleViewSet(SoftDeleteModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class RoleUserViewSet(SoftDeleteModelViewSet):
    queryset = RoleUser.objects.all()
    serializer_class = RoleUserSerializer


class ResourceViewSet(SoftDeleteModelViewSet):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer


class ResourceRoleViewSet(SoftDeleteModelViewSet):
    queryset = ResourceRole.objects.all()
    serializer_class = ResourceRoleSerializer

