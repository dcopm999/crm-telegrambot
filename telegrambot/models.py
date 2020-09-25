# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class Subscriber(models.Model):
    id = models.PositiveIntegerField(primary_key=True, verbose_name=_('Subscriber ID'))
    is_bot = models.BooleanField(verbose_name=_('Is bot'))
    first_name = models.CharField(max_length=250, verbose_name=_('First name'))
    language_code = models.CharField(max_length=7, choices=settings.LANGUAGES, verbose_name=_('Language code'))
    created = models.DateTimeField(auto_now_add=True, editable=False)
    edited = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return f'{self.first_name}: ({self.id})'

    class Meta:
        verbose_name = _('Subscriber')
        verbose_name_plural = _('Subscribers')


class Request(models.Model):
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE, verbose_name=_('Subscriber'))
    text = models.TextField(verbose_name=_('Text'))
    created = models.DateTimeField(auto_now_add=True, editable=False)
    edited = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = _('Request')
        verbose_name_plural = ('Requests')


class Response(models.Model):
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE, verbose_name=_('Subscriber'))
    text = models.TextField(verbose_name=_('Text'))
    created = models.DateTimeField(auto_now_add=True, editable=False)
    edited = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = _('Response')
        verbose_name_plural = ('Responses')


class Dialog(models.Model):
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE, verbose_name=_('Subscriber'))
    request = models.ForeignKey(Request, on_delete=models.CASCADE, verbose_name=_('Request'))
    response = models.ForeignKey(Response, on_delete=models.CASCADE, verbose_name=_('Response'))
    created = models.DateTimeField(auto_now_add=True, editable=False)
    edited = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.subscriber.__str__()

    class Meta:
        verbose_name = _('Dialog')
        verbose_name_plural = _('Dialogs')
