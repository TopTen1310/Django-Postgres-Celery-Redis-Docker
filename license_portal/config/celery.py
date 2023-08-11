import os
from celery import Celery
from datetime import timedelta
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
app = Celery('licenses')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.timezone = 'Europe/London'

app.conf.beat_schedule = {
    'every_midnight': {
        'task': 'licenses.tasks.check_and_send_email',
        'schedule': crontab(hour=0, minute=0)
    }
}

app.autodiscover_tasks()