import openai
import asyncio
import g4f
import html


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
            model='gpt-3.5-turbo',
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
        gpt_messages.append({'role': 'system', 'content': f"Now you are not an assistant, answer normally as a human being, behave like a normal person, imitate yourself just like the person described here: : {per_desc}"})

    for message in messages:
        gpt_messages.append({'role': message['sender'], 'content': message['text']})

    return gpt_messages

