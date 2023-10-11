from django.shortcuts import render
from rest_framework import generics
from .models import *
from .serializers import *


class GetUserChatsById(generics.ListAPIView):
    serializer_class = CreateChatSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        queryset = Chat.objects.filter(chat_user_id=user_id)
        return queryset


class GetChatById(generics.ListAPIView):
    serializer_class = ChatsWithMessagesListSerializer

    def get_queryset(self):
        chat_id = self.kwargs['chat_id']
        queryset = Chat.objects.get(id=chat_id)
        return queryset


class CreateNewChat(generics.CreateAPIView):
    model = Chat
    serializer_class = CreateChatSerializer


class SendMessage(generics.CreateAPIView):
    serializer_class = MessageSerializer

    def perform_create(self, serializer):
        chat_id = self.request.data.get('chat_id')
        chat = Chat.objects.get(id=chat_id)
        serializer.save(chat=chat)



