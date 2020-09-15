import logging
from  telebot import TeleBot
from django.conf import settings

logger = logging.getLogger(__name__)


class TelegramBot:
    def __init__(self, *args, **kwargs):
        self.TOKEN = settings.TELEGRAM_TOKEN
        self.bot = TeleBot(self.TOKEN)
        self.webhook_url = f'https://{settings.TELEGRAM_WEBHOOK_HOST}{settings.TELEGRAM_WEBHOOK_PATH}:443'
        self.bot.set_webhook(url=self.webhook_url)
        super(TelegramBot, self).__init__(*args, **kwargs)

    def __del__(self):
        self.bot.remove_webhook()
