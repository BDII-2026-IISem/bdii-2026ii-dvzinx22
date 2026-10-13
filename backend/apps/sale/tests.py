from decimal import Decimal
from unittest.mock import patch
from django.db.models import ManyToManyField, RestrictedError
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APITestCase
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


class SaleTransactionTests(APITestCase):
    def setUp(self):
        self.buyer = Client.objects.create(name="Comprador", status=RecordStatus.ACTIVE)
        product_type = ProductType.objects.create(name="Abarrote", status=RecordStatus.ACTIVE)
        self.water = Product.objects.create(
            product_type=product_type,
            name="Agua",
            price=Decimal("10.00"),
            stock=5,
            status=RecordStatus.ACTIVE,
        )
        self.bread = Product.objects.create(
            product_type=product_type,
            name="Pan",
            price=Decimal("4.50"),
            stock=2,
            status=RecordStatus.ACTIVE,
        )

    def _payload(self, items, discounts="0.00"):
        return {
            "clientId": self.buyer.id,
            "saleDate": timezone.now().isoformat(),
            "discounts": discounts,
            "items": items,
        }

    def test_register_snapshots_price_and_discounts_stock(self):
        """AC-11-01 y AC-11-02: Totales correctos, snapshot de precio y descuento de inventario."""
        response = self.client.post(
            "/api/sales/",
            self._payload(
                [
                    {"productId": self.water.id, "quantity": 2},
                    {"productId": self.bread.id, "quantity": 1},
                ],
                discounts="1.50",
            ),
            format="json",
        )
        self.assertEqual(response.status_code, 201, response.data)
        self.assertEqual(response.data["tax"], "0.00")
        self.assertEqual(response.data["subtotal"], "24.50")
        self.assertEqual(response.data["total"], "23.00")
        self.assertEqual(response.data["status"], "active")
        water_line = next(
            line for line in response.data["lines"] if line["product"] == self.water.id
        )
        self.assertEqual(water_line["unit_price"], "10.00")
        self.water.refresh_from_db()
        self.bread.refresh_from_db()
        self.assertEqual(self.water.stock, 3)
        self.assertEqual(self.bread.stock, 1)

        # AC-11-02: Precio histórico se mantiene si el catálogo cambia después
        self.water.price = Decimal("99.00")
        self.water.save()
        sale_obj = Sale.objects.get(pk=response.data["id"])
        line = sale_obj.lines.get(product=self.water)
        self.assertEqual(line.unit_price, Decimal("10.00"))

    def test_insufficient_stock_rolls_back(self):
        """AC-11-03: Stock insuficiente responde 400 y no crea la venta."""
        response = self.client.post(
            "/api/sales/",
            self._payload([{"productId": self.bread.id, "quantity": 3}]),
            format="json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Sale.objects.count(), 0)
        self.bread.refresh_from_db()
        self.assertEqual(self.bread.stock, 2)

    def test_stock_failure_rolls_back_the_sale(self):
        """AC-11-04: Fallo inesperado en guardado revierte Sale y ProductSale completamente."""
        original = Product.save

        def fail_stock(product, *args, **kwargs):
            update_fields = kwargs.get("update_fields")
            if update_fields and "stock" in update_fields:
                raise RuntimeError("fallo de stock")
            return original(product, *args, **kwargs)

        with patch.object(Product, "save", fail_stock):
            with self.assertRaises(RuntimeError):
                self.client.post(
                    "/api/sales/",
                    self._payload([{"productId": self.water.id, "quantity": 1}]),
                    format="json",
                )
        self.assertEqual(Sale.objects.count(), 0)
        self.assertEqual(ProductSale.objects.count(), 0)

    def test_inactive_client_is_rejected(self):
        """AC-11-05: Cliente inactivo responde 400 y no crea venta."""
        self.buyer.status = RecordStatus.INACTIVE
        self.buyer.save()
        response = self.client.post(
            "/api/sales/",
            self._payload([{"productId": self.water.id, "quantity": 1}]),
            format="json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Sale.objects.count(), 0)
