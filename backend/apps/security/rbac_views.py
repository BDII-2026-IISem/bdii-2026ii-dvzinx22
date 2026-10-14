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
