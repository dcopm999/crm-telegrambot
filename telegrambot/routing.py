from django.urls import path
from telegrambot.consumers import TelegramConsumer

urlpatterns = [
    path('telegram/', TelegramConsumer),
]
