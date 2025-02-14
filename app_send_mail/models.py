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


from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    birthday = models.DateField(null=True, blank=True)
    password = models.CharField(max_length=128)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.email

    def set_password(self, raw_password):
        """Хэширует и устанавливает пароль."""
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """Проверяет, соответствует ли введенный пароль хэшированному."""
        return check_password(raw_password, self.password)

class Newsletter(models.Model):
    subject = models.CharField(max_length=200)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.subject


class SentNewsletter(models.Model):
    newsletter = models.ForeignKey(Newsletter)
    subscriber = models.ForeignKey(Subscriber)
    sent_at = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(default=False)

    def __unicode__(self):
        return u"{} - {} - {}".format(self.newsletter.subject, self.subscriber.email, self.success)
