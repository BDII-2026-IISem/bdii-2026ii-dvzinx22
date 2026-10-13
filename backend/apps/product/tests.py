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


from rest_framework.test import APITestCase


class ProductApiTests(APITestCase):
    def setUp(self):
        self.product_type = ProductType.objects.create(
            name="Bebidas Calientes",
            description="Línea de cafés calientes de TazaNorte",
            status=RecordStatus.ACTIVE,
        )

    def test_product_type_crud(self):
        """CRUD de categorías: POST (201), GET (200), PATCH (200) y DELETE lógico (204)."""
        created = self.client.post(
            "/api/product-types/",
            {"name": "Repostería", "description": "Postres y panes frescos"},
            format="json",
        )
        self.assertEqual(created.status_code, 201)
        self.assertEqual(created.data["status"], RecordStatus.INACTIVE)
        pk = created.data["id"]

        self.assertEqual(self.client.get("/api/product-types/").status_code, 200)
        detail = self.client.get(f"/api/product-types/{pk}/")
        self.assertEqual(detail.data["name"], "Repostería")

        updated = self.client.patch(
            f"/api/product-types/{pk}/",
            {"status": "active"},
            format="json",
        )
        self.assertEqual(updated.status_code, 200)

        deleted = self.client.delete(f"/api/product-types/{pk}/")
        self.assertEqual(deleted.status_code, 204)
        self.assertEqual(ProductType.objects.get(pk=pk).status, RecordStatus.INACTIVE)

    def test_product_retrieve_update_and_soft_delete(self):
        """AC-09-01: Producto activo con stock aparece en catálogo, se actualiza y aplica baja lógica."""
        created = self.client.post(
            "/api/products/",
            {
                "productTypeId": self.product_type.id,
                "name": "Café Moca Especial",
                "price": "6500.00",
                "stock": 10,
                "status": "active",
            },
            format="json",
        )
        self.assertEqual(created.status_code, 201)
        pk = created.data["id"]

        detail = self.client.get(f"/api/products/{pk}/")
        self.assertEqual(detail.status_code, 200)
        self.assertEqual(detail.data["name"], "Café Moca Especial")

        updated = self.client.patch(f"/api/products/{pk}/", {"stock": 15}, format="json")
        self.assertEqual(updated.status_code, 200)
        self.assertEqual(updated.data["stock"], 15)

        deleted = self.client.delete(f"/api/products/{pk}/")
        self.assertEqual(deleted.status_code, 204)
        self.assertEqual(Product.objects.get(pk=pk).status, RecordStatus.INACTIVE)

    def test_default_status_and_type_restriction(self):
        """AC-09-03: Defaults status=inactive y stock=0. Borrado de tipo con hijos restringido."""
        created = self.client.post(
            "/api/products/",
            {"productTypeId": self.product_type.id, "name": "Infusión Frutal", "price": "3500.00"},
            format="json",
        )
        self.assertEqual(created.status_code, 201)
        self.assertEqual(created.data["status"], "inactive")
        self.assertEqual(created.data["stock"], 0)

        with self.assertRaises(RestrictedError):
            self.product_type.delete()

    def test_duplicate_product_name(self):
        """AC-09-02: Nombre de producto duplicado responde 400 Bad Request."""
        payload = {"productTypeId": self.product_type.id, "name": "Café Filtrado", "price": "4000.00"}
        self.assertEqual(self.client.post("/api/products/", payload, format="json").status_code, 201)
        self.assertEqual(self.client.post("/api/products/", payload, format="json").status_code, 400)
        self.assertEqual(Product.objects.get(name="Café Filtrado").price, Decimal("4000.00"))
