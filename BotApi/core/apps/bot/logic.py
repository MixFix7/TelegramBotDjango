import openai
import asyncio
import g4f
import html
import sys
from .bot_messges import *


_providers = [
    g4f.Provider.Aichat,
    g4f.Provider.ChatBase,
    g4f.Provider.Bing,
    g4f.Provider.CodeLinkAva,
    g4f.Provider.DeepAi,
    g4f.Provider.GptGo,
    g4f.Provider.Wewordle,
    g4f.Provider.You,
    g4f.Provider.Yqcloud
]


async def run_provider(provider: g4f.Provider.AsyncProvider, chat_messages) -> object:
    print(chat_messages)
    try:
        response = await provider.create_async(
            model='gpt-4',
            messages=chat_messages
        )
        print(f"{provider.__name__}:", response)
        return response

    except Exception as e:
        print(f"{provider.__name__}:", e)
        return f"Error: {e}"


async def get_message_from_gpt(chat_messages):
    return await asyncio.gather(run_provider(g4f.Provider.GptGo, chat_messages))


async def chatm_to_gptchatm(messages, per_desc):
    gpt_messages = []

    if per_desc:
        gpt_messages.append(
            {'role': 'system', 'content': f"{prompt_for_gpt4} {per_desc}"}
        )

    for message in messages:
        gpt_messages.append({'role': message['sender'], 'name': message['name'], 'content': message['text']})

    print(sys.getsizeof(gpt_messages))

    while sys.getsizeof(gpt_messages) >= 240:
        del gpt_messages[1]

    return gpt_messages

