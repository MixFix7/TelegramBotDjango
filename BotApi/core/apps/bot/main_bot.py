import telebot
import requests

from telebot.async_telebot import AsyncTeleBot
from telebot import State
from telebot import types

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

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for chat in response.json():
            chat_name = chat['name']
            button = types.KeyboardButton(chat_name)
            keyboard.add(button)

        await bot.send_message(message.chat.id, select_chat_message, reply_markup=keyboard)
        state[message.from_user.id] = 'select_chat'

    except Exception as e:
        await bot.send_message(message.chat.id, f"Error: {e}")


"""STATE COMMANDS HANDLERS"""


@bot.message_handler(func=lambda message: state.get(message.from_user.id) is None)
async def handle_unknown_command(message):
    await bot.send_message(message.chat.id, unknown_command_message, parse_mode="HTML")


# @bot.message_handler(func=lambda message: state.get(message.from_user.id) == 'speaking_with_bot')
# async def speak_with_chatbot(message):
#     gpt_answer = await logic.get_message_from_gpt(message.text)
#     await bot.send_message(message.chat.id, gpt_answer[0])


@bot.message_handler(func=lambda message: state.get(message.from_user.id).startswith('talking_with_chatbot'))
async def send_message_chatbot(message):
    try:
        user_id = message.from_user.id
        chat_id = int(state.get(user_id)[22:])
        sender_name = message.from_user.first_name
        text = message.text

        data = {
            'chat_id': chat_id,
            'text': text,
            'sender': sender_name
        }

        response = requests.post(f"{server_url}/chats/send-message/", data=data)

        if response.status_code == 201:
            await send_message_from_chatbot(message)
        else:
            await bot.send_message(message.chat.id, "Failed to send message")

    except Exception as e:
        await bot.send_message(message.chat.id, f"Error: {e}")


@bot.message_handler(func=lambda message: state.get(message.from_user.id) == 'new_chat')
async def start_new_chat(message):
    try:
        data = {
            'name': message.text,
            'chat_user_id': message.from_user.id,
            'chat_username': message.from_user.first_name
        }

        response = requests.post(f"{server_url}/chats/create-new-chat/", data=data)

        await bot.send_message(message.chat.id, chat_created_successfully)
    except Exception as e:
        await bot.send_message(message.chat.id, f'Error: {e}')


@bot.message_handler(func=lambda message: state.get(message.from_user.id) == 'select_chat')
async def open_selected_chat(message):
    chat_name = message.text
    response = requests.get(f"{server_url}/chats/get-chat-by-name/{chat_name}/")
    chat_data = response.json()
    state[message.from_user.id] = f"talking_with_chatbot: {chat_data['id']}"

    reply_keyboard = types.ReplyKeyboardRemove()
    await bot.send_message(message.chat.id, f"You in chat: {chat_data['name']}", reply_markup=reply_keyboard)


async def send_message_from_chatbot(message):
    try:
        chat_id = state.get(message.from_user.id)[22:]
        response = requests.get(f"{server_url}/chats/get-chat-by-id/{chat_id}/")

        if response.status_code != 200:
            await bot.send_message(message.chat.id, "Error, please try later")
            return

        chat = response.json()

        gpt_messages = await logic.chatm_to_gptchatm(chat['messages'], chat['personality_description'])
        gpt_answer = await logic.get_message_from_gpt(gpt_messages)

        response_save_message = await save_gpt_message(gpt_messages[0], chat['id'])

        if response_save_message == 201:
            await bot.send_message(message.chat.id, gpt_answer[0])
        else:
            await bot.send_message(message.chat.id, 'Error')

    except Exception as e:
        await bot.send_message(message.chat.id, f"Error: {e}")


async def save_gpt_message(text, chat_id):
    data = {
        'sender': 'Bot',
        'text': text,
        'chat_id': chat_id,
    }

    response = requests.post(f"{server_url}/chats/send-message/", data=data)
    return response.status_code
