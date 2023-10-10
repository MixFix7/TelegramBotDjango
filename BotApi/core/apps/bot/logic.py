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


async def run_provider(provider: g4f.Provider.AsyncProvider, message: str) -> object:
    try:
        response = await provider.create_async(
            model=g4f.models.default.name,
            messages=[{'role': 'user', 'content': message}]
        )
        print(f"{provider.__name__}:", response)
        return response

    except Exception as e:
        print(f"{provider.__name__}:", e)
        return f"Error: {e}"


async def run_all(message):
    return await asyncio.gather(run_provider(g4f.Provider.You, message))


def text_to_html(text):
    return html.escape(text)

