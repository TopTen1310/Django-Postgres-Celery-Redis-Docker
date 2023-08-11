from rest_framework import serializers

from licenses.models import Notification, Client, LicenseNotification


class ClientSerializer(serializers.ModelSerializer):
    admin_poc_email = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = ["client_name", "poc_contact_name",
                  "poc_contact_email", "admin_poc_email"]

    def get_admin_poc_email(self, obj: Client) -> str:
        return obj.admin_poc.email


class NotificationSerializer(serializers.ModelSerializer):
    client = ClientSerializer(read_only=True)
    expiring_license_count = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ["client", "expiring_license_count", "created"]

    def get_expiring_license_count(self, obj: Notification) -> int:
        return obj.licensenotification_set.all().count()
