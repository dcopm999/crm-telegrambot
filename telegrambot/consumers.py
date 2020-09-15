from channels.generic.http import AsyncHttpConsumer
from telegrambot.bot import TelegramBot


class TelegramConsumer(TelegramBot, AsyncHttpConsumer):
    async def handle(self, request):
        await self.send_response(200, b"Your response bytes", headers=[
            (b"Content-Type", b"text/plain"),
        ])
