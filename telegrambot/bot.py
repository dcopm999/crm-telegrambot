import logging

from allauth.socialaccount.models import SocialApp
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from products import models
from telebot import TeleBot, apihelper, types

logger = logging.getLogger(__name__)


class TelegramBot:
    def __init__(self):
        social_app = SocialApp.objects.last()
        TELEGRAM_TOKEN = social_app.secret
        TELEGRAM_WEBHOOK_HOST = social_app.sites.last().domain
        TELEGRAM_WEBHOOK_PATH = reverse("telegrambot:webhook")
        self.bot = TeleBot(TELEGRAM_TOKEN)
        self.WEBHOOK_URL = f"https://{TELEGRAM_WEBHOOK_HOST}{TELEGRAM_WEBHOOK_PATH}"
        logger.debug("%s: __init__()", self.__class__)

    def send_message(self, chat_id: int, text: str, reply_markup=None):
        try:
            self.bot.send_message(chat_id, text, reply_markup=reply_markup)
        except apihelper.ApiTelegramException as msg:
            logger.exception(msg)
        logger.debug(f"{self.__class__}: send_message({chat_id}, {text})")

    def send_photo(
        self, chat_id: str, photo_path: str, caption=None, reply_markup=None
    ):
        with open(photo_path, "rb") as photo_file:
            photo = photo_file.read()
        try:
            self.bot.send_photo(
                chat_id, photo=photo, caption=caption, reply_markup=reply_markup
            )
        except apihelper.ApiTelegramException as msg:
            logger.exception(msg)
            logger.info(f"{self.__class__}: User {chat_id} baned your TelegramBot")
        else:
            logger.debug(f"{self.__class__}: send_photo({chat_id}, {photo_path})")

    def answer_callback_query(
        self, callback_id, text=None, show_alert=None, url=None, cache_time=None
    ):
        self.bot.answer_callback_query(
            callback_id,
            text=text,
            show_alert=show_alert,
            url=url,
            cache_time=cache_time,
        )

    def set_webhook(self):
        logger.debug("%s: set_hook() %s" % (self.__class__, self.WEBHOOK_URL))
        return self.bot.set_webhook(url=self.WEBHOOK_URL)

    def remove_webhook(self):
        logger.debug("%s: remove_webhook()", self.__class__)
        return self.bot.remove_webhook()

    def get_kb_phone(self):
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button_phone = types.KeyboardButton(
            text="Отправить номер телефона", request_contact=True
        )
        button_geo = types.KeyboardButton(
            text="Отправить местоположение", request_location=True
        )
        keyboard.add(button_phone, button_geo)
        return keyboard

    def get_kb_catalog(self):
        keyboard = types.ReplyKeyboardMarkup(
            row_width=1, resize_keyboard=True, one_time_keyboard=True
        )
        buttons = [
            types.KeyboardButton(text=item.name)
            for item in models.Catalog.objects.all()
        ]
        keyboard.add(*buttons)
        return keyboard

    def get_kb_inline_buy(self, product):
        keyboard = types.InlineKeyboardMarkup()
        buy = _("Buy")
        text = f"{buy}: {product.name}"
        buy_btn = types.InlineKeyboardButton(text, callback_data=str(product.id))
        keyboard.add(buy_btn)
        return keyboard
