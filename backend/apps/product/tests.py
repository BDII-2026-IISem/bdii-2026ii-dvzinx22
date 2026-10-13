from decimal import Decimal
from django.db import IntegrityError
from django.db.models import RestrictedError
from django.test import TestCase
from apps.common.status import RecordStatus
from apps.product.models import Product, ProductType


class ProductModelTests(TestCase):
    def setUp(self):
        self.category = ProductType.objects.create(
            name="Café Caliente",
            description="Bebidas calientes a base de café espresso para TazaNorte",
        )

    def test_ac_05_01_product_type_required(self):
        """AC-05-01: product_type_id es obligatorio en la clave foránea."""
        with self.assertRaises(IntegrityError):
            Product.objects.create(
                product_type=None,
                name="Café Americano",
                price=Decimal("4500.00"),
            )

    def test_ac_05_02_delete_type_restricted(self):
        """AC-05-02: borrar el tipo con productos asociados lanza RestrictedError (EVI-05-02)."""
        Product.objects.create(
            product_type=self.category,
            name="Café Espresso",
            price=Decimal("4000.00"),
            stock=15,
        )
        with self.assertRaises(RestrictedError):
            self.category.delete()

    def test_ac_05_03_duplicate_product_name_rejected(self):
        """AC-05-03: el nombre de producto es único."""
        Product.objects.create(
            product_type=self.category,
            name="Capuchino Especial",
            price=Decimal("6000.00"),
        )
        with self.assertRaises(IntegrityError):
            Product.objects.create(
                product_type=self.category,
                name="Capuchino Especial",
                price=Decimal("6500.00"),
            )

    def test_ac_05_04_default_status_and_stock(self):
        """AC-05-04: status y stock por defecto son inactive y 0."""
        product = Product.objects.create(
            product_type=self.category,
            name="Latte Vainilla",
            price=Decimal("7000.00"),
        )
        self.assertEqual(product.status, RecordStatus.INACTIVE)
        self.assertEqual(product.stock, 0)
        self.assertEqual(self.category.status, RecordStatus.INACTIVE)

    def test_db_tables_and_metadata(self):
        """Verificación de nombres físicos de tablas según estándar."""
        self.assertEqual(ProductType._meta.db_table, "product_types")
        self.assertEqual(Product._meta.db_table, "products")
