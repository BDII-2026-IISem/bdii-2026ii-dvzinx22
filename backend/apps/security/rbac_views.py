from django.contrib.auth import get_user_model
from rest_framework import status, viewsets
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from apps.common.status import RecordStatus
from apps.security.models import Resource, ResourceRole, Role, RoleUser
from apps.security.permissions import HasResourceAccess
from apps.security.serializers import (
    ProfileSerializer,
    ResourceRoleSerializer,
    ResourceSerializer,
    RoleSerializer,
    RoleUserSerializer,
    UserSerializer,
)

User = get_user_model()


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


class SoftDeleteModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, HasResourceAccess]
    lookup_value_converter = "int"

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if hasattr(instance, "status"):
            instance.status = RecordStatus.INACTIVE
            instance.save(update_fields=["status"])
            return Response(status=status.HTTP_204_NO_CONTENT)
        if hasattr(instance, "is_active"):
            instance.is_active = False
            instance.save(update_fields=["is_active"])
            return Response(status=status.HTTP_204_NO_CONTENT)
        return super().destroy(request, *args, **kwargs)


class UserViewSet(SoftDeleteModelViewSet):
    queryset = User.objects.all().order_by("id")
    serializer_class = UserSerializer


class RoleViewSet(SoftDeleteModelViewSet):
    queryset = Role.objects.all().order_by("id")
    serializer_class = RoleSerializer


class RoleUserViewSet(SoftDeleteModelViewSet):
    queryset = RoleUser.objects.all().select_related("user", "role").order_by("id")
    serializer_class = RoleUserSerializer


class ResourceViewSet(SoftDeleteModelViewSet):
    queryset = Resource.objects.all().order_by("id")
    serializer_class = ResourceSerializer


class ResourceRoleViewSet(SoftDeleteModelViewSet):
    queryset = ResourceRole.objects.all().select_related("role", "resource").order_by("id")
    serializer_class = ResourceRoleSerializer
