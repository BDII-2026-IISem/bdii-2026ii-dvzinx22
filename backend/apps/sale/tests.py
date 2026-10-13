from decimal import Decimal
from django.db.models import ManyToManyField, RestrictedError
from django.test import TestCase
from django.utils import timezone
from apps.client.models import Client
from apps.common.status import RecordStatus
from apps.product.models import Product, ProductType
from apps.sale.models import ProductSale, Sale


class SaleModelTests(TestCase):
    def setUp(self):
        self.client = Client.objects.create(
            name="Carlos Ramirez",
            email="carlos.ramirez@tazanorte.com",
            status=RecordStatus.ACTIVE,
        )
        self.product_type = ProductType.objects.create(
            name="Cafetería Caliente",
            description="Bebidas de café para TazaNorte",
            status=RecordStatus.ACTIVE,
        )
        self.product = Product.objects.create(
            product_type=self.product_type,
            name="Café Espresso Doble",
            price=Decimal("4500.00"),
            stock=20,
            status=RecordStatus.ACTIVE,
        )

    def test_ac_06_01_db_table_names(self):
        """AC-06-01: existen tablas sales y product_sales."""
        self.assertEqual(Sale._meta.db_table, "sales")
        self.assertEqual(ProductSale._meta.db_table, "product_sales")

    def test_ac_06_02_foreign_key_restrict(self):
        """AC-06-02: las llaves foráneas usan on_delete=RESTRICT."""
        sale = Sale.objects.create(
            client=self.client,
            sale_date=timezone.now(),
            total=Decimal("9000.00"),
            status=RecordStatus.ACTIVE,
        )
        ProductSale.objects.create(
            sale=sale,
            product=self.product,
            quantity=2,
            unit_price=self.product.price,
            line_total=Decimal("9000.00"),
            status=RecordStatus.ACTIVE,
        )
        with self.assertRaises(RestrictedError):
            self.client.delete()
        with self.assertRaises(RestrictedError):
            self.product.delete()

    def test_ac_06_03_line_total_calculated_on_save(self):
        """AC-06-03: line_total se calcula automáticamente como cantidad * unit_price."""
        sale = Sale.objects.create(
            client=self.client,
            sale_date=timezone.now(),
            status=RecordStatus.ACTIVE,
        )
        line = ProductSale.objects.create(
            sale=sale,
            product=self.product,
            quantity=3,
            unit_price=Decimal("4500.00"),
            line_total=Decimal("0.00"),
            status=RecordStatus.ACTIVE,
        )
        self.assertEqual(line.line_total, Decimal("13500.00"))

    def test_ac_06_04_no_many_to_many_field(self):
        """AC-06-04: no existe ManyToManyField entre Sale y Product."""
        m2m_fields = [f for f in Sale._meta.get_fields() if isinstance(f, ManyToManyField)]
        self.assertEqual(len(m2m_fields), 0)

    def test_evi_06_02_historical_price_preserved(self):
        """EVI-06-02: el precio histórico se conserva al modificar el precio del producto."""
        sale = Sale.objects.create(
            client=self.client,
            sale_date=timezone.now(),
            status=RecordStatus.ACTIVE,
        )
        line = ProductSale.objects.create(
            sale=sale,
            product=self.product,
            quantity=2,
            unit_price=self.product.price,
            line_total=Decimal("0.00"),
            status=RecordStatus.ACTIVE,
        )
        # Se actualiza el precio del producto posteriormente
        self.product.price = Decimal("6000.00")
        self.product.save()

        line.refresh_from_db()
        self.assertEqual(line.unit_price, Decimal("4500.00"))
        self.assertEqual(line.line_total, Decimal("9000.00"))

    def test_void_sale_restitutes_stock(self):
        """La anulación de la venta restituye el stock de los productos vendidos a TazaNorte."""
        sale = Sale.objects.create(
            client=self.client,
            sale_date=timezone.now(),
            status=RecordStatus.ACTIVE,
        )
        ProductSale.objects.create(
            sale=sale,
            product=self.product,
            quantity=5,
            unit_price=self.product.price,
            line_total=Decimal("0.00"),
            status=RecordStatus.ACTIVE,
        )
        self.product.stock = 15
        self.product.save()

        sale.void()
        self.product.refresh_from_db()
        sale.refresh_from_db()

        self.assertEqual(self.product.stock, 20)
        self.assertEqual(sale.status, RecordStatus.INACTIVE)
