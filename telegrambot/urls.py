# -*- coding: utf-8 -*-
from django.urls import path
from django.views.generic import TemplateView

from . import views


app_name = 'telegrambot'
urlpatterns = [
    path(r'', TemplateView.as_view(template_name="base.html")),
]
