import telebot
import requests

from telebot.async_telebot import AsyncTeleBot
from telebot import State

from django.conf import settings
from asgiref.sync import sync_to_async

from .bot_messges import *
from . import logic

from core.apps.chats.models import *


bot = AsyncTeleBot(settings.BOT_TOKEN, parse_mode='HTML')

state = {}
server_url = 'http://localhost:8000'


async def main():
    webhook_url = 'http://localhost:8000/tg-bot/telegram-bot-webhook/'
    await bot.remove_webhook()
    await bot.set_webhook(url=webhook_url)


"""COMMANDS HANDLERS"""


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


@bot.message_handler(commands=['list_chats'])
async def select_chat_from_list(message):
    try:
        response = requests.get(f"{server_url}/chats/get-user-chats-by-id/{message.from_user.id}/")
        print(response.json())

        for chat in response.json():
            await bot.send_message(message.chat.id, chat['name'])

    except Exception as e:
        await bot.send_message(message.chat.id, f"Error: {e}")


@bot.message_handler(func=lambda message: state.get(message.from_user.id) is None)
async def handle_unknown_command(message):
    await bot.send_message(message.chat.id, unknown_command_message, parse_mode="HTML")


"""STATE COMMANDS HANDLERS"""


@bot.message_handler(func=lambda message: state.get(message.from_user.id) == 'speaking_with_bot')
async def chatbot_message(message):
    gpt_answer = await logic.run_all(message.text)
    await bot.send_message(message.chat.id, gpt_answer[0])


@bot.message_handler(func=lambda message: state.get(message.from_user.id) == 'new_chat')
async def start_new_chat(message):
    try:
        print(message)
        data = {
            'name': message.text,
            'chat_user_id': message.from_user.id,
            'chat_username': message.from_user.first_name
        }

        response = requests.post(f"{server_url}/chats/create-new-chat/", data=data)
        print(response.status_code)
 
        await bot.send_message(message.chat.id, chat_created_successfully)
    except Exception as e:
        await bot.send_message(message.chat.id, f'Error: {e}')












