from django.core.management.base import BaseCommand, CommandError
import asyncio

from core.apps.bot.main_bot import bot, main


class Command(BaseCommand):
    help = 'Launch the telegram bot'

    def handle(self, *args, **options):
        loop = asyncio.get_event_loop()

        asyncio.run(bot.polling())
        loop.run_until_complete(main())


