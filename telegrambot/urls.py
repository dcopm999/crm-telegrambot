# -*- coding: utf-8 -*-
from django.urls import path
from django.views.generic import TemplateView


app_name = 'telegrambot'
urlpatterns = [
    path(r'', TemplateView.as_view(template_name="base.html")),
]
