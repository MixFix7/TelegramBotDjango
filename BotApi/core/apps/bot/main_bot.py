import telebot
from telebot.async_telebot import AsyncTeleBot
from telebot import State
from django.conf import settings
from .bot_messges import *
from . import logic

from core.apps.chats.models import *


bot = AsyncTeleBot(settings.BOT_TOKEN, parse_mode='HTML')

state = {}


async def main():
    webhook_url = 'http://localhost:8000/tg-bot/telegram-bot-webhook/'
    await bot.remove_webhook()
    await bot.set_webhook(url=webhook_url)


@bot.message_handler(commands=['start'])
async def send_welcome(message):
    await bot.reply_to(message, welcome_message)


@bot.message_handler(commands=['speaking_with_bot'])
async def handle_speaking_with_chatbot(message):
    await bot.send_message(message.chat.id, you_talking_with + '<strong>Chatbot</strong>')
    await bot.send_message(message.chat.id, to_exit)
    state[message.from_user.id] = 'speaking_with_bot'


@bot.message_handler(func=lambda message: state.get(message.from_user.id) == 'speaking_with_bot')
async def chatbot_message(message):
    gpt_answer = logic.generate_response(message.text)
    await bot.send_message(message.chat.id, gpt_answer)


@bot.message_handler(commands=['new_chat'])
async def handle_new_chat(message):
    await bot.send_message(message.chat.id, please_write_name_for_chat)
    state[message.from_user.id] = 'new_chat'


@bot.message_handler(func=lambda message: state.get(message.from_user.id) == 'new_chat')
async def start_new_chat(message):
    new_chat_data = {
        'chat_id': message.chat.id,
        'name': message.text,
        'chat_username': message.sender.id,
    }

    try:
        Chat.objects.create(new_chat_data)
        await bot.send_message(message.chat.id, chat_created_successfully)
    except Exception as e:
        await bot.send_message(message.chat.id, error_message)


@bot.message_handler(commands=['quit'])
async def quit(message):
    await bot.send_message(message.chat.id, you_out)
    state[message.from_user.id] = None



