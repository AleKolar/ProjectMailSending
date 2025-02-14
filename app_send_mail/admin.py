from django.contrib import admin
from .models import Subscriber, Newsletter, SentNewsletter

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'birthday', 'subscribed_at')
    search_fields = ('email','first_name', 'last_name', 'birthday', 'subscribed_at')

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('subject', 'body', 'created_at')
    search_fields = ('subject',)

@admin.register(SentNewsletter)
class SentNewsletterAdmin(admin.ModelAdmin):
    list_display = ('newsletter', 'subscriber', 'success', 'sent_at')
    search_fields = ('newsletter__subject', 'subscriber__email', 'subscriber__first_name', 'subscriber__last_name', 'subscriber__birthday', 'subscriber__subscribed_at',)
