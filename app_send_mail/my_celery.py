import os
from celery import Celery
from django.conf import settings
import django
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

django.setup()

app = Celery('mysite')

app.config_from_object('django.conf:settings')

app.autodiscover_tasks(settings.INSTALLED_APPS)

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

app.conf.update(
    worker_log_level='INFO',
    broker_url='amqp://guest:guest@localhost:5672//',
    accept_content=['json'],
    task_serializer='json',
    result_serializer='json',
)

app.conf.beat_schedule = {
    'send-weekly-article-list': {
        'task': 'news.tasks.send_email_notification_to_subscribers',
        'schedule': crontab(day_of_week='monday', hour=8, minute=0),
    },
}