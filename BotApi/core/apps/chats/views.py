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


class GetChatById(generics.RetrieveAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    lookup_field = 'id'


class GetChatByName(generics.RetrieveAPIView):
    queryset = Chat.objects.all()  # Define the queryset to include all chats
    serializer_class = ChatSerializer
    lookup_field = 'name'  # Set the lookup field to 'name' for searching by chat name


class CreateNewChat(generics.CreateAPIView):
    model = Chat
    serializer_class = CreateChatSerializer


class SendMessage(generics.CreateAPIView):
    serializer_class = MessageCreateSerializer

    def perform_create(self, serializer):
        chat_id = self.request.data.get('chat_id')
        chat = Chat.objects.get(id=chat_id)
        serializer.save(chat=chat)



