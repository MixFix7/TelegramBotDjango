from django.core.management.base import BaseCommand, CommandError
import asyncio

from core.apps.bot.main_bot import bot


class Command(BaseCommand):
    help = 'Launch the telegram bot'

    def handle(self, *args, **options):
        asyncio.run(bot.polling())


