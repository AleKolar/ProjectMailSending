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



class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    birthday = models.DateField(null=True, blank=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.email


class Newsletter(models.Model):
    subject = models.CharField(max_length=200)
    body = models.TextField()  # ????? ????? HTML ?????
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):  # ??? Python 2.7
        return self.subject


class SentNewsletter(models.Model):
    newsletter = models.ForeignKey(Newsletter)
    subscriber = models.ForeignKey(Subscriber)
    sent_at = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(default=False)

    def __unicode__(self):  # ??? Python 2.7
        return u"{} - {} - {}".format(self.newsletter.subject, self.subscriber.email, self.success)
