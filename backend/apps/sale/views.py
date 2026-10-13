from drf_spectacular.utils import extend_schema
from rest_framework import mixins, status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.sale.models import Sale
from apps.sale.serializers import SaleRegisterSerializer, SaleSerializer


class SaleRegisterAPIView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=SaleRegisterSerializer,
        responses={201: SaleSerializer},
    )
    def post(self, request):
        serializer = SaleRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        sale = serializer.save()
        sale = Sale.objects.prefetch_related("lines__product").get(pk=sale.pk)
        return Response(SaleSerializer(sale).data, status=status.HTTP_201_CREATED)


class SaleReadViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """Lectura y anulación lógica de ventas en TazaNorte.

    GET /api/sales/         → listado (ListModelMixin.list)
    GET /api/sales/<pk>/    → detalle (RetrieveModelMixin.retrieve)
    DELETE /api/sales/<pk>/ → anulación (DestroyModelMixin.destroy → Sale.void)
    """

    queryset = (
        Sale.objects.select_related("client")
        .prefetch_related("lines__product")
        .order_by("-sale_date", "-id")
    )
    serializer_class = SaleSerializer
    permission_classes = [AllowAny]
    lookup_value_converter = "int"

    def perform_destroy(self, instance):
        instance.void()


class SaleCollectionAPIView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(responses=SaleSerializer(many=True))
    def get(self, request, *args, **kwargs):
        sales = SaleReadViewSet.queryset.all()
        return Response(SaleSerializer(sales, many=True).data)

    @extend_schema(
        request=SaleRegisterSerializer,
        responses={201: SaleSerializer},
    )
    def post(self, request, *args, **kwargs):
        handler = SaleRegisterAPIView()
        handler.request = request
        handler.format_kwarg = None
        handler.args = ()
        handler.kwargs = {}
        return handler.post(request)
