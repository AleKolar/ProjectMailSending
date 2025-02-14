
from celery import shared_task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from .models import Subscriber, SentNewsletter, Newsletter
from django.conf import settings

@shared_task
def send_newsletter_task(newsletter_id):
    newsletter = Newsletter.objects.get(id=newsletter_id)
    subscribers = Subscriber.objects.all()
    subject = newsletter.subject
    body = newsletter.body

    for subscriber in subscribers:
        try:
            html_content = render_to_string('newsletter.html', {
                'subscriber': subscriber,
                'subject': subject,
                'body': body
            })
            msg = EmailMessage(subject, html_content, settings.DEFAULT_FROM_EMAIL, [subscriber.email])
            msg.content_subtype = "html"
            msg.send()

            SentNewsletter.objects.create(newsletter=newsletter, subscriber=subscriber, success=True)
        except Exception as e:
            SentNewsletter.objects.create(newsletter=newsletter, subscriber=subscriber, success=False)
            print("Error sending to {subscriber.email}: {e}")