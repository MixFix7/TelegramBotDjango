from telebot.async_telebot import AsyncTeleBot
from django.conf import settings
from .bot_messges import *
from . import logic

bot = AsyncTeleBot(settings.BOT_TOKEN, parse_mode='HTML')


print('Bot started successfully!!!')


async def main():
    webhook_url = 'http://localhost:8000/tg-bot/telegram-bot-webhook/'
    await bot.remove_webhook()
    await bot.set_webhook(url=webhook_url)


@bot.message_handler(commands=['start'])
async def send_welcome(message):
    await bot.reply_to(message, welcome_message)


@bot.message_handler(func=lambda message: True)
async def echo_all(message):
    gpt_answer = logic.generate_response(message.text)
    await bot.send_message(message.chat.id, gpt_answer)

