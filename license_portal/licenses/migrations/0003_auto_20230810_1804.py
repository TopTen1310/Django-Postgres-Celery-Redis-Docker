# Generated by Django 3.2 on 2023-08-10 18:04
import sys
import uuid

from dateutil.relativedelta import relativedelta
from django.db import migrations, models
import django.db.models.deletion
from django.utils import timezone

from licenses.models import LicenseType, Package


def create_test_data(apps, schema_editor) -> None:
    # Create only if not testing
    if sys.argv[1:2] == ["test"]:
        return

    # We get the model from the versioned app registry;
    # if we directly import it, it'll be the wrong version
    from django.contrib.auth.models import User

    admin = User.objects.create(
        username="admin", is_staff=True, is_superuser=True)
    admin.set_password("admin")
    admin.save()

    Client = apps.get_model("licenses", "Client")
    License = apps.get_model("licenses", "License")

    User = apps.get_model("auth", "User")
    staff_a = User.objects.create(
        username="Staff A", email=f"test.admin@{uuid.uuid4().hex}.com", is_staff=True)
    staff_b = User.objects.create(
        username="Staff B", email=f"test.admin@{uuid.uuid4().hex}.com", is_staff=True)

    client_a = Client.objects.create(
        client_name="Client A",
        poc_contact_name="Client A of Staff A",
        poc_contact_email=f"test.client@{uuid.uuid4().hex}.com",
        admin_poc=staff_a,
    )
    client_b = Client.objects.create(
        client_name="Client B",
        poc_contact_name="Client B of Staff A",
        poc_contact_email=f"test.client@{uuid.uuid4().hex}.com",
        admin_poc=staff_a,
    )
    client_c = Client.objects.create(
        client_name="Client C",
        poc_contact_name="Client C of Staff B",
        poc_contact_email=f"test.client@{uuid.uuid4().hex}.com",
        admin_poc=staff_b,
    )

    time_now = timezone.now()
    four_months_from_now = time_now + relativedelta(months=4)
    one_week_from_now = time_now + relativedelta(days=7)

    expiring_license_a1 = License.objects.create(
        license_type=LicenseType.production.value,
        package=Package.ios_sdk.value,
        expiration_datetime=four_months_from_now,
        client=client_a,
    )
    expiring_license_b1 = License.objects.create(
        license_type=LicenseType.evaluation.value,
        package=Package.javascript_sdk.value,
        expiration_datetime=four_months_from_now,
        client=client_b,
    )
    expiring_license_c1 = License.objects.create(
        license_type=LicenseType.production.value,
        package=Package.javascript_sdk.value,
        expiration_datetime=one_week_from_now,
        client=client_c,
    )


def remove_test_data(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("licenses", "0002_auto_20220520_1009"),
    ]

    operations = [
        migrations.AlterField(
            model_name="License",
            name="license_type",
            field=models.PositiveSmallIntegerField(
                choices=[(LicenseType.production.value, "production"),
                         (LicenseType.evaluation.value, "evaluation")]
            ),
        ),
        migrations.AlterField(
            model_name="License",
            name="package",
            field=models.PositiveSmallIntegerField(
                choices=[(Package.javascript_sdk.value, "javascript_sdk"),
                         (Package.ios_sdk.value, "ios_sdk"), (Package.android_sdk.value, "android_sdk")]
            ),
        ),
        migrations.CreateModel(
            name="Notification",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                (
                    "client",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="licenses.client",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="LicenseNotification",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "notification_type",
                    models.PositiveSmallIntegerField(
                        choices=[(0, "four_month"),
                                 (1, "one_month"), (2, "one_week")]
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                (
                    "license",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="licenses.license",
                    ),
                ),
                (
                    "notification",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="licenses.notification",
                    ),
                ),
            ],
        ),
        migrations.RunPython(create_test_data, remove_test_data),
    ]