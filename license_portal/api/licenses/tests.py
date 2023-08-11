import email
import json
import uuid
from unittest.mock import patch

from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase, Client as APIClient
from django.utils import timezone
from freezegun import freeze_time
from rest_framework import status
from django.urls import reverse

from licenses.models import (
    Client,
    License,
    LicenseType,
    Package,
)


@freeze_time("2023-02-18T15:00")
class LicenseExpiryTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user_a = User.objects.create(username="User A")
        cls.client_a = Client.objects.create(
            client_name="Client A",
            poc_contact_name="Client Admin A",
            poc_contact_email=f"test.client@{uuid.uuid4().hex}.com",
            admin_poc=cls.user_a,
        )
        time_now = timezone.now()
        four_months_from_now = time_now + relativedelta(months=4)

        cls.expiring_license_a1 = License.objects.create(
            license_type=LicenseType.production.value,
            package=Package.ios_sdk.value,
            expiration_datetime=four_months_from_now,
            client=cls.client_a,
        )

    def setUp(self) -> None:
        self.api_client = APIClient()

    def test_api_flow(self) -> None:
        # Test the POST endpoint
        # Patch the send_notification method
        with patch('licenses.tasks.EmailNotification.send_notification') as mock_send_notification:
            response = self.api_client.post(
                '/api/license/?page=1',
                headers={"content-type": "application/json"}
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            # Check if the send_notification method was called
            self.assertTrue(mock_send_notification.called)

            response_content = json.loads(response.content)
            self.assertEqual(len(response_content["results"]), 1)
            self.assertEqual(response_content["results"][0]["expiring_license_count"], 1)
            self.assertEqual(response_content["results"][0]["client"]["client_name"], "Client A")

        # Test the GET endpoint
        response = self.api_client.get(
            '/api/license/?page=1',
            headers={"content-type": "application/json"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        response_content = json.loads(response.content)
        self.assertEqual(len(response_content["results"]), 1)
        self.assertEqual(response_content["results"][0]["expiring_license_count"], 1)
        self.assertEqual(response_content["results"][0]["client"]["client_name"], "Client A")
