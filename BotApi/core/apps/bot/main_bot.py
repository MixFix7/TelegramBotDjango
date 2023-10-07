from telebot.async_telebot import AsyncTeleBot
from django.conf import settings
from .bot_messges import *

bot = AsyncTeleBot(settings.BOT_TOKEN, parse_mode='HTML')


@bot.message_handler(commands=['start'])
async def send_welcome(message):
    await bot.reply_to(message, welcome_message)


@bot.message_handler(func=lambda message: True)
async def echo_message(message):
    await bot.send_message(message.chat.id, message.text)
