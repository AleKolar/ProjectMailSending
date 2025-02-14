# -*- encoding: utf-8 -*-

# -*- coding: utf-8 -*-

#!/usr/bin/python
# -*- coding: latin-1 -*-
import os, sys


#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
import os, sys


#!/usr/bin/python
# -*- coding: ascii -*-
import os, sys

from django.http import JsonResponse
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

from django.contrib.auth.decorators import login_required
from rest_framework import viewsets

from .forms import NewsletterForm, SubscriberRegistrationForm
from .models import SentNewsletter, Newsletter
from .serializers import SubscriberSerializer
from .tasks import send_newsletter_task, send_newsletter_to_all


def home(request):
    return render(request, 'home.html')

def register(request):
    form = SubscriberRegistrationForm()
    if request.method == 'POST':
        form = SubscriberRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'register.html', {'form': form})


from django.shortcuts import render, redirect
from .models import Subscriber


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            subscriber = Subscriber.objects.get(email=email)
            if subscriber.check_password(password):
                request.session['subscriber_id'] = subscriber.id
                return render(request, 'dashboard.html')
        except Subscriber.DoesNotExist:
            return render(request, 'login.html', {'error': 'Неправильный email или пароль'})

    return render(request, 'login.html')

@login_required(login_url='login')
def create_newsletter(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            body = form.cleaned_data['message']

            # Создание новостной рассылки
            newsletter = Newsletter.objects.create(subject=subject, body=body)
            send_to_all = request.POST.get('sendToAllValue') == 'true'

            if send_to_all:
                # Получаем всех подписчиков
                subscriber_ids = Subscriber.objects.values_list('id', flat=True)
                send_newsletter_to_all.delay(list(subscriber_ids), subject, body)
            else:
                # Получаем значения для фильтрации
                first_name = request.POST.get('first_name', '')
                last_name = request.POST.get('last_name', '')
                birthday_day = request.POST.get('birthday_day', '')
                birthday_month = request.POST.get('birthday_month', '')
                birthday_year = request.POST.get('birthday_year', '')

                # Формируем фильтр для подписчиков
                kwargs = {}
                if first_name:
                    kwargs['first_name'] = first_name
                if last_name:
                    kwargs['last_name'] = last_name
                if birthday_day:
                    kwargs['birthday__day'] = birthday_day
                if birthday_month:
                    kwargs['birthday__month'] = birthday_month
                if birthday_year:
                    kwargs['birthday__year'] = birthday_year

                # Фильтрация подписчиков
                subscribers = Subscriber.objects.filter(**kwargs)

                # Отправка писем только отфильтрованным подписчикам
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

            return JsonResponse({'status': 'success', 'message': 'Newsletter created and sent!'})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})
    else:
        form = NewsletterForm()
        return render(request, 'newsletter.html', {'form': form})


# def filter_subscribers(request):
#     if request.method == 'GET':
#
#         first_name = request.GET.get('first_name')
#         last_name = request.GET.get('last_name')
#         birthday_day = request.GET.get('birthday_day')
#         birthday_month = request.GET.get('birthday_month')
#         birthday_year = request.GET.get('birthday_year')
#
#         kwargs = {}
#         if first_name:
#             kwargs['first_name'] = first_name
#         if last_name:
#             kwargs['last_name'] = last_name
#         if birthday_day:
#             kwargs['birthday__day'] = birthday_day
#         if birthday_month:
#             kwargs['birthday__month'] = birthday_month
#         if birthday_year:
#             kwargs['birthday__year'] = birthday_year
#
#         subscribers_filter = Subscriber.objects.filter(**kwargs)
#
#         email_lst = [subscriber.email for subscriber in subscribers_filter]
#         first_name_lst = [subscriber.first_name for subscriber in subscribers_filter]
#         last_name_lst = [subscriber.last_name for subscriber in subscribers_filter]
#         birthday_day_lst = [subscriber.birthday.day for subscriber in subscribers_filter]
#         birthday_month_lst = [subscriber.birthday.month for subscriber in subscribers_filter]
#         birthday_year_lst = [subscriber.birthday.year for subscriber in subscribers_filter]
#
#         context = {
#             'emails': email_lst,
#             'first_names': first_name_lst,
#             'last_names': last_name_lst,
#             'birthday_days': birthday_day_lst,
#             'birthday_months': birthday_month_lst,
#             'birthday_years': birthday_year_lst
#         }
#
#         return render(request, 'filter_subscribers.html', context)





# @csrf_exempt
# def send_newsletter(request):
#     if request.method == 'POST':
#         subject = request.POST.get('subject')
#         message = request.POST.get('message')
#
#         subscribers = Subscriber.objects.all()
#         email_list = [sub.email for sub in subscribers]
#
#         send_mail(subject, message, 'gefest-173@yandex.ru', email_list)
#         return JsonResponse({'status': 'success'})
#     return JsonResponse({'status': 'error'}, status=400)


class SubscriberViewSet(viewsets.ModelViewSet):
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer