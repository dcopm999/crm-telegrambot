import logging
from telebot import TeleBot, types, apihelper
#telebot.apihelper.ApiTelegramException
from django.conf import settings

from telegrambot import models as telegrambot_models
from products import models as product_models

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

    def send_message(self, chat_id:int, text:str, reply_markup=None):
        try:
            self.bot.send_message(chat_id, text, reply_markup=reply_markup)
        except apihelper.ApiTelegramException as msg:
            logger.exception(msg)
        logger.debug(f'{self.__class__}: send_message({chat_id}, {text})')

    def send_photo(self, chat_id: str, photo_path: str, caption=None):
        with open(photo_path, 'rb') as photo_file:
            photo = photo_file.read()
        self.bot.send_photo(chat_id, photo=photo, caption=caption)
        logger.debug(f'{self.__class__}: send_photo({chat_id}, {photo_path})')

    def set_webhook(self):
        logger.debug('%s: set_hook() %s' % (self.__class__, self.WEBHOOK_URL))
        return self.bot.set_webhook(url=self.WEBHOOK_URL)

    def remove_webhook(self):
        logger.debug('%s: remove_webhook()', self.__class__)
        return self.bot.remove_webhook()

    def get_kb_phone():
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button_phone = types.KeyboardButton(text="Отправить номер телефона", request_contact=True)
        button_geo = types.KeyboardButton(text="Отправить местоположение", request_location=True)
        keyboard.add(button_phone, button_geo)
        return keyboard

    def get_kb_catalog(self):
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        buttons = [types.KeyboardButton(text=item.name) for item in product_models.Catalog.objects.all()]
        keyboard.add(*buttons)
        return keyboard

