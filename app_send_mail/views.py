from django.shortcuts import render
from django.http import JsonResponse
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from app_send_mail.forms import NewsletterForm, SubscriberRegistrationForm
from app_send_mail.models import SentNewsletter, Newsletter, Subscriber


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

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'login.html')

@login_required(login_url='login')
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

