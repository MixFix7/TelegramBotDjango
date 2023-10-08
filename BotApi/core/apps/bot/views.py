from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings
from .main_bot import bot

import telebot

@csrf_exempt
@require_POST
def webhook(request):
    json_str = request.body.decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])

    return HttpResponse(status=200)

