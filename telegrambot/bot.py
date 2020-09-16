import logging
from  telebot import TeleBot
from django.conf import settings

logger = logging.getLogger(__name__)


class TelegramBot:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(TelegramBot, cls).__new__(cls)
        return cls.instance

    def __init__(self, *args, **kwargs):
        self.TOKEN = settings.TELEGRAM_TOKEN
        self.bot = TeleBot(self.TOKEN)
        self.WEBHOOK_URL = f'https://{settings.TELEGRAM_WEBHOOK_HOST}{settings.TELEGRAM_WEBHOOK_PATH}'
        
        super(TelegramBot, self).__init__(*args, **kwargs)

    def set_webhook(self):
        return self.bot.set_webhook(url=self.WEBHOOK_URL)

    def remove_webhook(self):
        return self.bot.remove_webhook()
