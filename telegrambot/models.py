# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Subscriber(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("User"))
    name = models.CharField(max_length=250, verbose_name=_("Name"))
    telegram_id = models.PositiveBigIntegerField(verbose_name=_("Telegram ID"))
    is_bot = models.BooleanField(default=False, verbose_name=_("Is bot"))
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.user.__str__()

    class Meta:
        verbose_name = _("Subscriber")
        verbose_name_plural = _("Subscribers")


class Request(models.Model):
    subscriber = models.ForeignKey(
        Subscriber, on_delete=models.CASCADE, verbose_name=_("Subscriber")
    )
    text = models.TextField(verbose_name=_("Text"))
    created = models.DateTimeField(auto_now_add=True, editable=False)
    edited = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = _("Request")
        verbose_name_plural = "Requests"


class Response(models.Model):
    subscriber = models.ForeignKey(
        Subscriber, on_delete=models.CASCADE, verbose_name=_("Subscriber")
    )
    text = models.TextField(verbose_name=_("Text"))
    created = models.DateTimeField(auto_now_add=True, editable=False)
    edited = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = _("Response")
        verbose_name_plural = "Responses"


class Dialog(models.Model):
    subscriber = models.ForeignKey(
        Subscriber, on_delete=models.CASCADE, verbose_name=_("Subscriber")
    )
    request = models.ForeignKey(
        Request, on_delete=models.CASCADE, verbose_name=_("Request")
    )
    response = models.ForeignKey(
        Response, on_delete=models.CASCADE, verbose_name=_("Response")
    )
    created = models.DateTimeField(auto_now_add=True, editable=False)
    edited = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.subscriber.__str__()

    class Meta:
        verbose_name = _("Dialog")
        verbose_name_plural = _("Dialogs")
        ordering = ["-created"]
