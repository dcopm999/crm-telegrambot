import json
import logging

from channels.generic.http import AsyncHttpConsumer

from telegrambot.handlers import HandlerCommandStart, HandlerCommandHelp

logger = logging.getLogger(__name__)


class TelegramConsumer(AsyncHttpConsumer):
    handlers = [HandlerCommandStart, HandlerCommandHelp]

    async def handle(self, body):
        logger.debug('%s: handle()', self.__class__)
        body = json.loads(body)
        self.get_handler().handle(body)
        await self.send_response(
            200,
            b"OK",
            headers=[(b"Content-Type", b"text/plain")]
        )

    def get_handler(self):
        logger.debug('%s: get_handler()', self.__class__)
        before = None
        for handler in self.handlers:
            if before is None:
                before = handler()
                result = before
            else:
                before.set_next(handler())
                before = handler()
        logger.debug('%s: result=%s' % (self.__class__, result))
        return result
