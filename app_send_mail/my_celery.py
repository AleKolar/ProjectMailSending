# import os
# from celery import Celery
# from django.conf import settings
# import django
# from celery.schedules import crontab
#
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
#
# django.setup()
#
# installed_apps = settings.INSTALLED_APPS
#
# debug_mode = settings.DEBUG
# database_settings = settings.DATABASES
#
# app = Celery('api')
#
# app.config_from_object('django.conf:settings')
#
# app.autodiscover_tasks('tasks')
#
# @app.task(bind=True, ignore_result=True)
# def debug_task(self):
#     print('Request: {self.request!r}')
#
# CELERY_BROKER_URL = 'amqp://guest:guest@localhost:5672'
# CELERY_ACCEPT_CONTENT = ['json']
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_RESULT_SERIALIZER = 'json'
#
#
#
#
# app.conf.update(
#     worker_log_level='INFO'
# )
#
# # app.conf.beat_schedule = {
# #     'send-weekly-article-list': {
# #         'task': 'path.to.send_weekly_article_list',
# #         'schedule': crontab(day_of_week='monday', hour=8, minute=0),
# #     },
# # }
# app.conf.beat_schedule = {
#     'send-weekly-article-list': {
#         'task': 'news.tasks.send_email_notification_to_subscribers',
#         'schedule': crontab(day_of_week='monday', hour=8, minute=0),
#     },
# }