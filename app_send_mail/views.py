from django.shortcuts import render
from django.http import JsonResponse
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

from app_send_mail.forms import NewsletterForm
from app_send_mail.models import SentNewsletter, Newsletter, Subscriber


def create_newsletter(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            body = form.cleaned_data['body']


            newsletter = Newsletter.objects.create(subject=subject, body=body)

            subscribers = Subscriber.objects.all()
            for subscriber in subscribers:
                try:
                    html_content = render_to_string('newsletter_template.html', {
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

            return JsonResponse({'status': 'success', 'message': 'Newsletter created and sent!'})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})
    else:
        form = NewsletterForm()
        return render(request, 'newsletter_form.html', {'form': form})

