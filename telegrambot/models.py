# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


class Request(models.Model):
    subscriber = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name=_('Subscriber'))
    text = models.TextField(verbose_name=_('Text'))
    created = models.DateTimeField(auto_now_add=True, editable=False)
    edited = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = _('Request')
        verbose_name_plural = ('Requests')


class Response(models.Model):
    subscriber = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name=_('Subscriber'))
    text = models.TextField(verbose_name=_('Text'))
    created = models.DateTimeField(auto_now_add=True, editable=False)
    edited = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = _('Response')
        verbose_name_plural = ('Responses')


class Dialog(models.Model):
    subscriber = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name=_('Subscriber'))
    request = models.ForeignKey(Request, on_delete=models.CASCADE, verbose_name=_('Request'))
    response = models.ForeignKey(Response, on_delete=models.CASCADE, verbose_name=_('Response'))
    created = models.DateTimeField(auto_now_add=True, editable=False)
    edited = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.subscriber.__str__()

    class Meta:
        verbose_name = _('Dialog')
        verbose_name_plural = _('Dialogs')
        ordering = ['-created']
