from django.test import TransactionTestCase
from django.core.files import File
from django.contrib.auth.models import User

from ...update import (
    update_aged_creditor_facts_v2,
)
from ...utils import import_data
from ...models import (
    AgedCreditorFactsV2,
    AgedCreditorFactsV2Update,
)

from ..resources import AgedCreditorFactsV2Resource


FIXTURES_PATH = "municipal_finance/fixtures/tests/update/aged_creditor_facts_v2"


class UpdateAgedCreditorFactsV2(TransactionTestCase):
    serialized_rollback = True

    def setUp(self):
        import_data(
            AgedCreditorFactsV2Resource,
            f"{FIXTURES_PATH}/aged_creditor_facts_v2.csv",
        )
        self.user = User.objects.create_user(
            username="sample", email="sample@some.co", password="testpass",
        )
        self.insert_obj = AgedCreditorFactsV2Update.objects.create(
            user=self.user,
            file=File(open(f"{FIXTURES_PATH}/insert.csv", "rb")),
        )
        self.update_obj = AgedCreditorFactsV2Update.objects.create(
            user=self.user,
            file=File(open(f"{FIXTURES_PATH}/update.csv", "rb")),
        )

    def test_without_updates(self):
        self.assertEqual(AgedCreditorFactsV2.objects.all().count(), 15)
        update_aged_creditor_facts_v2(
            self.insert_obj,
            batch_size=4,
        )
        self.assertEqual(AgedCreditorFactsV2.objects.all().count(), 25)
        self.assertEqual(self.insert_obj.deleted, 0)
        self.assertEqual(self.insert_obj.inserted, 10)

    def test_with_updates(self):
        self.assertEqual(AgedCreditorFactsV2.objects.all().count(), 15)
        update_aged_creditor_facts_v2(
            self.update_obj,
            batch_size=4,
        )
        self.assertEqual(AgedCreditorFactsV2.objects.all().count(), 25)
        self.assertEqual(self.update_obj.deleted, 5)
        self.assertEqual(self.update_obj.inserted, 15)
