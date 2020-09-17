import logging
from abc import ABC, abstractmethod
from typing import Any, Optional, List

from telegrambot.bot import TelegramBot

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


class HandlerCommandBase(AbstractHandler):
    command: List[Handler]

    def handle(self, request: Any) -> str:
        logger.debug('%s: handle()', self.__class__)
        print(request)
        if request.get('message').get('text') == self.command:
            self.run(request)
        else:
            super().handle(request)

    @abstractmethod
    def run(self, request: Any):
        logger.debug('%s: run()', self.__class__)
        self.bot.send_message(request.get('message').get('chat').get('id'), 'started')


class HandlerCommandStart(HandlerCommandBase):
    command: List[Handler] = '/start'

    def run(self, request: Any):
        logger.debug('%s: run()', self.__class__)
        self.bot.send_message(request.get('message').get('chat').get('id'), 'started')


class HandlerCommandHelp(HandlerCommandBase):
    command = '/help'

    def run(self, request: Any):
        logger.debug('%s: run()', self.__class__)
        self.bot.send_message(request.get('message').get('chat').get('id'), 'Helped')
