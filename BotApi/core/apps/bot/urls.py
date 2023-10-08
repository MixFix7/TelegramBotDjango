from django.urls import path
from . import views

urlpatterns = [
    path('telegram-bot-webhook/', views.webhook, name='webhook')
]
