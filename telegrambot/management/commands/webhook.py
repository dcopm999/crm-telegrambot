import logging
from django.core.management.base import BaseCommand, CommandError
from telegrambot.bot import TelegramBot

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'TelegramBot webhook management'

    def add_arguments(self, parser):
        parser.add_argument(
            'action',
            type=str,
            help='[set, remove]',
        )

    def handle(self, *args, **kwargs):
        bot = TelegramBot()
        if kwargs['action'] == 'set':
            if bot.set_webhook():
                self.stdout.write(self.style.SUCCESS(f'Set TelegramBot WebHook to {bot.WEBHOOK_URL}: success'))
                logger.debug('Set TelegramBot WebHook to %s: success', bot.WEBHOOK_URL)
            else:
                logger.error('Set TelegramBot WebHook to %s: error', bot.WEBHOOK_URL)
                raise CommandError(self.style.ERROR(f'Set TelegramBot WebHook to {bot.WEBHOOK_URL}: error'))

        elif kwargs['action'] == 'remove':
            if bot.remove_webhook():
                self.stdout.write(self.style.SUCCESS(f'Remove TelegramBot WebHook to {bot.WEBHOOK_URL}: success'))
                logger.debug('Remove TelegramBot WebHook to %s: success', bot.WEBHOOK_URL)
            else:
                logger.error('Remove TelegramBot WebHook to %s: error', bot.WEBHOOK_URL)
                raise CommandError(self.style.ERROR(f'Remove TelegramBot WebHook to {bot.WEBHOOK_URL}: error'))
