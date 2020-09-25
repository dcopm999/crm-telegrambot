# -*- coding: utf-8 -*-
from django.urls import path

from telegrambot import views


app_name = 'telegrambot'
urlpatterns = [
    path('', views.WebhookView.as_view(), name='webhook')
]
