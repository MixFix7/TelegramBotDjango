from rest_framework import serializers
from rest_framework import serializers
from .models import Message, Chat  # Import your Message and Chat models


class MessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class MessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['sender', 'text']


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['id', 'name', 'chat_user_id', 'personality_description', 'messages']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        messages = instance.messages.all()
        data['messages'] = MessagesSerializer(messages, many=True).data
        return data


class CreateChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'
