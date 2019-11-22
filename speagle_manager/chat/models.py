from django.db import models
from django.utils.translation import ugettext_lazy as _

import os
from binascii import hexlify


class Thread(models.Model):
    hash_id = models.CharField(_("hashed id"), max_length=50, default=str(hexlify(os.urandom(16)), 'ascii'),unique=True)
    title = models.CharField(_("title"), max_length=50)
    created = models.DateTimeField(_("created"), auto_now=False, auto_now_add=True)
    users = models.ManyToManyField("accounts.User", verbose_name=_("users"), blank=True)
    last_messages = models.ForeignKey("chat.Message", verbose_name=_("message"), on_delete=models.SET_NULL, blank=True, null=True)


class Message(models.Model):
    hash_id = models.CharField(_("hashed id"), max_length=50, default=str(hexlify(os.urandom(16)), 'ascii'),unique=True)
    sent = models.DateTimeField(_("sent datetime"), auto_now=False, auto_now_add=True)
    text = models.CharField(_("text"), max_length=1024)
    thread = models.ForeignKey("chat.Thread", verbose_name=_("thread"), on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey("accounts.User", verbose_name=_("sender"), on_delete=models.SET_NULL, null=True)


class UnreadMessages(models.Model):
    sent = models.DateTimeField(_("sent datetime"), auto_now=False, auto_now_add=True)
    message = models.ForeignKey("chat.Message", verbose_name=_("message"), on_delete=models.CASCADE, related_name='unread')
    thread = models.ForeignKey("chat.Thread", verbose_name=_("thread"), on_delete=models.CASCADE, related_name='unread')
    sender = models.ForeignKey("accounts.User", verbose_name=_("sender"), on_delete=models.CASCADE, related_name='unread')