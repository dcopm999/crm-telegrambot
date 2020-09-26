import logging
from abc import ABC, abstractmethod
from typing import Any, Optional
from telegrambot.bot import TelegramBot
from telegrambot.mixins import HistoryMixin, CatalogMixin

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
    command: str

    def handle(self, request: Any) -> str:
        logger.debug('%s: handle()', self.__class__)
        if request.get('callback_query', False) or request.get('message').get('text') == self.command or self.command == '__all__':
            self.run(request)
        super().handle(request)

    def run(self, request):
        return None

    def get_result(self):
        return None


class HandlerCommandStart(HistoryMixin, HandlerCommandBase):
    command = '/start'

    def run(self, request):
        logger.debug('%s: run()', self.__class__)
        if request.get('message'):
            chat_id = request.get('message').get('chat').get('id')
            keyboard = self.bot.get_kb_catalog()
            self.bot.send_message(chat_id, 'Catalog', reply_markup=keyboard)
        super(HandlerCommandStart, self).run(request)

    def get_result(self):
        return 'started'


class HandlerCommandHelp(HandlerCommandBase):
    command = '/help'

    def get_result(self):
        return 'helped'


class HandlerProductList(CatalogMixin, HandlerCommandBase):
    command = '__all__'

    def run(self, request):
        if request.get('message'):
            chat_id = request.get('message').get('chat').get('id')
            category = request.get('message').get('text')
            products = self.get_product_by_categoty(category)
            if products is None:
                pass
            else:
                for product in products:
                    buy_btn = self.bot.get_kb_inline_buy(product)
                    self.bot.send_photo(chat_id, product.image.path, product.caption, buy_btn)


class HandlerProductOrder(CatalogMixin, HandlerCommandBase):
    command = '__all__'

    def run(self, request):
        if request.get('callback_query'):
            chat_id = request.get('callback_query').get('message').get('chat').get('id')
            product_id = request.get('callback_query').get('data')
            self.set_product_order(chat_id=chat_id, product_id=product_id)
