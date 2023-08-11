from datetime import timedelta
from typing import List

from celery import shared_task
from celery.utils.log import get_task_logger

from dateutil.relativedelta import relativedelta
from django.db.models import Q, Exists, Subquery, OuterRef, Prefetch, QuerySet
from django.utils import timezone
from licenses.notifications import EmailNotification

from licenses.models import (
    License,
    Client,
    NotificationType,
    Notification,
    LicenseNotification
)

logger = get_task_logger(__name__)


def _get_time_conditions() -> Q:
    time_now = timezone.now()
    four_months_from_now = time_now + relativedelta(months=4)
    one_month_from_now = time_now + relativedelta(months=1)
    one_week_from_now = time_now + timedelta(days=7)

    four_months_from_now_qs = Q(
        expiration_datetime__lt=four_months_from_now + timedelta(days=1),
        expiration_datetime__gt=four_months_from_now - timedelta(days=1),
    ) & ~Q(licensenotification__notification_type=NotificationType.four_month.value)  # Skip if the license is already sent this notification

    one_month_from_now_qs = Q(
        expiration_datetime__lt=one_month_from_now,
        expiration_datetime__gt=one_week_from_now,
    ) & ~Q(licensenotification__notification_type=NotificationType.one_month.value)  # Skip if the license is already sent this notification

    within_a_week = Q(
        expiration_datetime__lte=one_week_from_now,
    ) & ~Q(licensenotification__notification_type=NotificationType.one_week.value)  # Skip if the license is already sent this notification

    time_conditions = four_months_from_now_qs | within_a_week
    if timezone.now().weekday() == 0:  # Check whether today is Monday
        time_conditions |= one_month_from_now_qs
    return time_conditions


def get_clients_with_expiring_licenses() -> QuerySet:
    time_conditions = _get_time_conditions()
    return (
        Client.objects.annotate(
            expiring_licenses_exist=Exists(
                Subquery(License.objects.filter(
                    time_conditions, client=OuterRef("id")))
            )
        )
        .filter(expiring_licenses_exist=True)
        .prefetch_related(
            Prefetch(
                "license_set",
                queryset=License.objects.filter(time_conditions).distinct(),
                to_attr="expiring_licenses",
            )
        )
        .distinct()
    )


def _create_notification(client) -> Notification:
    notification = Notification.objects.create(client=client)

    license_notifications = []
    for license in client.expiring_licenses:
        license_notifications.append(
            LicenseNotification(
                license=license,
                notification=notification,
                notification_type=LicenseNotification.get_notification_type(
                    license),
            )
        )
    LicenseNotification.objects.bulk_create(license_notifications)
    return notification


@shared_task(bind=True)
def check_and_send_email(self=None) -> List[Notification]:
    logger.info("**Start sending email for clients who have expiring licenses**")

    clients_with_expiring_licenses = get_clients_with_expiring_licenses()
    notifications = []

    for client in clients_with_expiring_licenses:
        EmailNotification.send_notification([client.admin_poc.email], {
            'client': client,
            'expiring_licenses': client.expiring_licenses
        })
        notification = _create_notification(client)
        notifications.append(notification)

    logger.info("**End sending email for clients who have expiring licenses**")

    return notifications


@shared_task()
def thirty_second_func():
    logger.info("I run every 30 seconds using Celery Beat")

    print('text from thirty second func')
    return 'Done'
