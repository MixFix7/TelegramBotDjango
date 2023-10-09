import telebot
from telebot.async_telebot import AsyncTeleBot
from telebot import State

from django.conf import settings
from asgiref.sync import sync_to_async

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


@bot.message_handler(commands=['quit'])
async def quit(message):
    await bot.send_message(message.chat.id, you_out)
    state[message.from_user.id] = None


@bot.message_handler(commands=['help'])
async def command_help(message):
    await bot.send_message(message.chat.id, list_of_commands)


@bot.message_handler(commands=['new_chat'])
async def handle_new_chat(message):
    await bot.send_message(message.chat.id, please_write_name_for_chat)
    state[message.from_user.id] = 'new_chat'


@bot.message_handler(commands=['speaking_with_bot'])
async def handle_speaking_with_chatbot(message):
    await bot.send_message(message.chat.id, you_talking_with)
    await bot.send_message(message.chat.id, to_exit)
    state[message.from_user.id] = 'speaking_with_bot'


@bot.message_handler(func=lambda message: state.get(message.from_user.id) is None)
async def handle_unknown_command(message):
    await bot.send_message(message.chat.id, unknown_command_message, parse_mode="HTML")


@bot.message_handler(func=lambda message: state.get(message.from_user.id) == 'speaking_with_bot')
async def chatbot_message(message):
    gpt_answer = logic.generate_response(message.text)
    await bot.send_message(message.chat.id, gpt_answer)


@bot.message_handler(func=lambda message: state.get(message.from_user.id) == 'new_chat')
async def start_new_chat(message):
    try:
        create_chat = sync_to_async(Chat.objects.create)

        print(message)

        await create_chat(
            chat_id=message.chat.id,
            name=message.text,
            chat_username=message.from_user.username,
        )
 
        await bot.send_message(message.chat.id, chat_created_successfully)
    except Exception as e:
        await bot.send_message(message.chat.id, f'Error: {e}')






