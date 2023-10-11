from rest_framework import serializers
from .models import *


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        modal = Message
        fields = '__all__'


class ChatsWithMessagesListSerializer(serializers.ListSerializer):

    class Meta:
        model = Chat
        fields = ['id', 'name', 'chat_user_id', 'personality_description']


class CreateChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'


