from typing import Any

from django.db.models import QuerySet
from rest_framework import status, generics
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from api.licenses.serializers import NotificationSerializer
from licenses.models import Notification
from licenses.tasks import (
    check_and_send_email
)


class LicenseView(GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = NotificationSerializer

    def get_queryset(self) -> QuerySet:
        """
        Return all notifications
        """
        return Notification.objects.all()

    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Get all notifications so far, paginated.

        Responses:
        - 200 OK: List of notifications after checking for license expiry
        [
            "client": {
                "client_name": client name who have expired licenses
            }
            "expiring_license_count": count of expired licenses,
            "created": date of this notification
        ]

        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Method to trigger check for license expiry, and then retrieve and paginate all notifications.

        Responses:
        - 200 OK: List of notifications after checking for license expiry
        {
            "notifications" : [
                "client": {
                    "client_name": client name who have expired licenses
                }
                "expiring_license_count": count of expired licenses,
                "created": date of this notification
            ],
            "triggered_notifications": length of triggered notifications
        }

        """
        notifications = check_and_send_email()

        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        response_data = {
            "notifications": serializer.data,
            "triggered_notifications": len(notifications)
        }
        return Response(response_data, status=status.HTTP_200_OK)
