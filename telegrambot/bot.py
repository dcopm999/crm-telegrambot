import logging
from  telebot import TeleBot
from django.conf import settings

logger = logging.getLogger(__name__)


class TelegramBot:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(TelegramBot, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.TOKEN = settings.TELEGRAM_TOKEN
        self.bot = TeleBot(self.TOKEN)
        self.WEBHOOK_URL = f'https://{settings.TELEGRAM_WEBHOOK_HOST}{settings.TELEGRAM_WEBHOOK_PATH}'
        logger.debug('%s: __init__()', self.__class__)

    def send_message(self, chat_id:int, text:str):
        self.bot.send_message(chat_id, text)
        logger.debug('%s: send_message(%i, %s)' % (self.__class__, chat_id, text))

    def set_webhook(self):
        logger.debug('%s: set_hook() %s' % (self.__class__, self.WEBHOOK_URL))
        return self.bot.set_webhook(url=self.WEBHOOK_URL)

    def remove_webhook(self):
        logger.debug('%s: remove_webhook()', self.__class__)
        return self.bot.remove_webhook()
