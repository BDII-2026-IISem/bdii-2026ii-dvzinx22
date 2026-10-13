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
