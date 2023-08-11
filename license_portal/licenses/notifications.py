from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.core.mail import get_connection

from typing import List, Any

from django.core.mail import send_mail, BadHeaderError
from django.template import Template
from django.template.loader import get_template

DEFAULT_FROM_EMAIL = 'noreply@email.com'


class EmailNotification:
    """ A convenience class to send email notifications
    """
    subject = 'License expiry info'  # type: str
    from_email = DEFAULT_FROM_EMAIL  # type: str
    template_path = 'license_expire_email.html'  # type: str

    @classmethod
    def load_template(cls) -> Template:
        """Load the configured template path"""
        return get_template(cls.template_path)

    @classmethod
    def send_notification(cls, recipients: List[str], context: Any) -> None:
        """Send the notification using the given context"""
        template = cls.load_template()
        message_body = template.render(context=context)
        try:
            send_mail(cls.subject, message_body, cls.from_email,
                      recipients, fail_silently=False)
        except BadHeaderError:
            print("Failed to send email. Please check email settings.")

        # *******************THIS IS FOR SMTP MAIL SERVER******************
        # with get_connection(
        #     host=settings.EMAIL_HOST,
        #     port=settings.EMAIL_PORT,
        #     username=settings.EMAIL_HOST_USER,
        #     password=settings.DONOT_REPLY_EMAIL_PASSWORD,
        #     use_tls=settings.EMAIL_USE_TLS
        # ) as connection:
        #     print("Email server connected!")
        #     msg = EmailMultiAlternatives(
        #         cls.subject,
        #         message_body,
        #         cls.from_email,
        #         recipients,
        #         cc=[],
        #         connection=connection)

        #     print(cls.subject,
        #           message_body,
        #           cls.from_email,
        #           recipients,)
        #     msg.send()
        # *****************************************************************
