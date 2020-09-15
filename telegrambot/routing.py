from django.urls import path
from channels.routing import URLRouter
from telegrambot.consumers import TelegramConsumer

application = URLRouter([
    path('telegram/', TelegramConsumer),
])
