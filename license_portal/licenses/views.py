from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from licenses.tasks import check_and_send_email

from licenses.models import Client, License, Notification
from licenses.notifications import EmailNotification


def email_template(request):
    client = Client.objects.last()
    license = License.objects.last()

    template = EmailNotification.load_template()
    email_body_html = template.render({
        "client": client,
        "expiring_licenses": [license]
    })
    return HttpResponse(email_body_html)
