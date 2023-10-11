from django.db import models
from datetime import datetime


class Chat(models.Model):
    name = models.CharField(max_length=100)
    chat_user_id = models.CharField(max_length=100)
    chat_username = models.CharField(max_length=100)
    personality_description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Chat with {self.chat_username}"


class Message(models.Model):
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)
    sender = models.CharField(max_length=200)
    text = models.TextField(null=True, blank=True)

    dispatch_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        message_dispatch_date = self.dispatch_date.strftime('%Y-%m-%d %H:%M:%S')
        return f"Message of {self.sender}, sent at {message_dispatch_date} "

