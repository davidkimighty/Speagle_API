from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

import os
from binascii import hexlify


class MessageThread(models.Model):
    title = models.CharField(_("title"), max_length=50, unique=True)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name=_("users"), blank=True)
    timestamp = models.DateTimeField(_("created"), auto_now_add=True)
    # unread_messages = models.ForeignKey('chat.Message', verbose_name=_("unread messages"), on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title


class Message(models.Model):
    # hash_id = models.CharField(_("hashed id"), max_length=50, default=str(hexlify(os.urandom(16)), 'ascii'), unique=True)
    thread = models.ForeignKey("chat.MessageThread", verbose_name=_("thread"), on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("sender"), on_delete=models.SET_NULL, null=True)
    text = models.TextField()
    timestamp = models.DateTimeField(_("sent datetime"), auto_now_add=True)

    def __str__(self):
        return self.sender.email

    def last_10_messages(self):
        return Message.objects.filter(thread=thread).order_by('-timestamp')[:10]


class Unreads(models.Model):
    message = models.ForeignKey('chat.Message', on_delete=models.CASCADE, related_name='unread')
    thread = models.ForeignKey('chat.MessageThread', on_delete=models.CASCADE, related_name='unread')
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='unread')
    timestamp = models.DateTimeField(_("sent datetime"), auto_now=False, auto_now_add=True)