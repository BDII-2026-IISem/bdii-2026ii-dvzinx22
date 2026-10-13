from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase
from apps.client.models import Client
from apps.common.status import RecordStatus

class ClientModelTests(TestCase):
    def test_ac_04_01_db_table_name(self):
        """AC-04-01: la tabla física es clients."""
        self.assertEqual(Client._meta.db_table, "clients")

    def test_ac_04_02_default_status_is_inactive(self):
        """AC-04-02: sin status en el alta, el valor es inactive."""
        client = Client.objects.create(name="Juan Perez")
        self.assertEqual(client.status, RecordStatus.INACTIVE)

    def test_ac_04_03_timestamps_generated(self):
        """AC-04-03: created_at y updated_at se generan automáticamente."""
        client = Client.objects.create(name="Maria Lopez")
        self.assertIsNotNone(client.created_at)
        self.assertIsNotNone(client.updated_at)

    def test_ac_04_04_duplicate_email_rejected(self):
        """AC-04-04: el email duplicado se rechaza."""
        Client.objects.create(name="Cliente Uno", email="test@example.com")
        with self.assertRaises(IntegrityError):
            Client.objects.create(name="Cliente Dos", email="test@example.com")

    def test_ac_04_05_short_name_rejected(self):
        """AC-04-05: un nombre de un carácter se rechaza por MinLengthValidator."""
        client = Client(name="A")
        with self.assertRaises(ValidationError):
            client.full_clean()

    def test_email_normalized_to_lowercase(self):
        """El método save() normaliza el correo electrónico a minúsculas."""
        client = Client.objects.create(name="Carlos Gomez", email="Carlos.Gomez@Domain.COM")
        self.assertEqual(client.email, "carlos.gomez@domain.com")


from decimal import Decimal
from djangorestframework_camel_case.render import CamelCaseJSONRenderer
from apps.client.serializers import ClientSerializer
from apps.product.models import Product, ProductType
from apps.product.serializers import ProductSerializer


class SerializerCamelCaseTests(TestCase):
    def test_ac_07_01_client_json_camel_case_created_at(self):
        """AC-07-01 (EVI-07-01): El JSON renderizado contiene createdAt y no created_at."""
        client = Client.objects.create(name="Maria Lopez", email="maria@example.com")
        serializer = ClientSerializer(client)
        renderer = CamelCaseJSONRenderer()
        rendered_bytes = renderer.render(serializer.data)
        content_str = rendered_bytes.decode("utf-8")

        self.assertIn('"createdAt"', content_str)
        self.assertNotIn('"created_at"', content_str)
        self.assertIn('"updatedAt"', content_str)

    def test_ac_07_02_email_normalized_and_empty_to_none(self):
        """AC-07-02: Maria@Example.com se normaliza a minúsculas y strings vacíos se vuelven None."""
        data = {
            "name": "Maria Lopez",
            "email": "Maria@Example.COM",
            "address": "",
            "phone": "",
        }
        serializer = ClientSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        client = serializer.save()
        self.assertEqual(client.email, "maria@example.com")
        self.assertIsNone(client.address)
        self.assertIsNone(client.phone)

    def test_ac_07_03_product_serializer_includes_product_type_name(self):
        """AC-07-03: El serializer de producto expone productTypeId y productTypeName en camelCase."""
        cat = ProductType.objects.create(name="Café Caliente")
        prod = Product.objects.create(
            product_type=cat,
            name="Café Espresso",
            price=Decimal("4000.00"),
            stock=10,
        )
        serializer = ProductSerializer(prod)
        renderer = CamelCaseJSONRenderer()
        rendered_bytes = renderer.render(serializer.data)
        content_str = rendered_bytes.decode("utf-8")

        self.assertIn('"productTypeId"', content_str)
        self.assertIn('"productTypeName"', content_str)
        self.assertIn("Café Caliente", content_str)
        self.assertEqual(serializer.data["product_type_name"], "Café Caliente")
