from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

import os
from binascii import hexlify


class Thread(models.Model):
    hash_id = models.CharField(_("hashed id"), max_length=50, default=str(hexlify(os.urandom(16)), 'ascii'),unique=True)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name=_("users"), blank=True)
    title = models.CharField(_("title"), max_length=50)
    timestamp = models.DateTimeField(_("created"), auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.hash_id


class Message(models.Model):
    hash_id = models.CharField(_("hashed id"), max_length=50, default=str(hexlify(os.urandom(16)), 'ascii'),unique=True)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("sender"), on_delete=models.SET_NULL, null=True)
    thread = models.ForeignKey("chat.Thread", verbose_name=_("thread"), on_delete=models.CASCADE, related_name='messages')
    text = models.TextField()
    timestamp = models.DateTimeField(_("sent datetime"), auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.sender.email

    def last_10_messages(self):
        return Message.objects.order_by('-timestamp').all()[:10]