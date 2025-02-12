from django.shortcuts import render
from django.http import JsonResponse
from django.core.mail import send_mail, EmailMessage
from django.template import Context, Template
from .forms import NewsletterForm
from .models import Subscriber, Newsletter, SentNewsletter
from django.conf import settings

def create_newsletter(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            body = form.cleaned_data['body']

            newsletter = Newsletter.objects.create(subject=subject, body=body)

            #  Отправка рассылки (упрощенный пример)
            subscribers = Subscriber.objects.all()
            for subscriber in subscribers:
                try:
                    # Используем EmailMessage для HTML-контента
                    msg = EmailMessage(subject, body, settings.DEFAULT_FROM_EMAIL, [subscriber.email])
                    msg.content_subtype = "html"  # Важно для HTML-писем
                    msg.send()

                    SentNewsletter.objects.create(newsletter=newsletter, subscriber=subscriber, success=True)
                except Exception as e:
                    SentNewsletter.objects.create(newsletter=newsletter, subscriber=subscriber, success=False)
                    # Логирование ошибки
                    print "Error sending to {}: {}".format(subscriber.email, e)


            return JsonResponse({'status': 'success', 'message': 'Newsletter created and sent!'})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})
    else:
        form = NewsletterForm()
        return render(request, 'newsletter_form.html', {'form': form})  # Или возвращаем пустую форму 

