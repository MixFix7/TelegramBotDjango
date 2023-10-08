import openai
import asyncio
from django.conf import settings


openai.api_key = settings.OPENAI_API_KEY


def generate_response(message):
    prompt = f"System: 'Hello you are friendly assistant. Your model is GPT-4' \nUser: {message}"

    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=400,
    )

    return response.choices[0].text

