import logging
from abc import ABC, abstractmethod
from typing import Any, Optional
from telegrambot.bot import TelegramBot
from telegrambot.mixins import HistoryMixin
from telegrambot import models

logger = logging.getLogger(__name__)


class Handler(ABC):
    """
    Интерфейс Обработчика объявляет метод построения цепочки обработчиков. Он
    также объявляет метод для выполнения запроса.
    """

    @abstractmethod
    def set_next(self, handler):
        pass

    @abstractmethod
    def handle(self, request) -> Optional[str]:
        pass


class AbstractHandler(Handler):
    """
    Поведение цепочки по умолчанию может быть реализовано внутри базового класса
    обработчика.
    """
    _next_handler: Handler = None

    def __init__(self):
        logger.debug('%s: __init__()', self.__class__)
        self.bot = TelegramBot()

    def set_next(self, handler: Handler) -> Handler:
        logger.debug('%s: set_next()', self.__class__)
        self._next_handler = handler
        logger.debug('%s: self._next_handler=%s' % (self.__class__, handler))
        # Возврат обработчика отсюда позволит связать обработчики простым
        # способом, вот так:
        # monkey.set_next(squirrel).set_next(dog)
        return handler

    @abstractmethod
    def handle(self, request: Any) -> str:
        if self._next_handler:
            return self._next_handler.handle(request)
        return None


class HandlerCommandBase(HistoryMixin, AbstractHandler):
    command: str

    def handle(self, request: Any) -> str:
        logger.debug('%s: handle()', self.__class__)
        if request.get('message').get('text') == self.command or self.command == '__all__':
            self.run(request)
        super().handle(request)

    def run(self, request):
        logger.debug('%s: run()', self.__class__)
        chat_id = request.get('message').get('chat').get('id')
        self.bot.send_message(chat_id, self.get_result())
        super(HandlerCommandBase, self).run(request)

    @abstractmethod
    def get_result(self):
        return None


class HandlerCommandStart(HandlerCommandBase):
    command = '/start'

    def get_result(self):
        return 'started'


class HandlerCommandHelp(HandlerCommandBase):
    command = '/help'

    def get_result(self):
        return 'helped'
