from django.urls import path
from .views import *


urlpatterns = [
    path('get-user-chats-by-id/<str:user_id>/', GetUserChatsById.as_view()),
    path('get-chat-by-id/<str:name>/', GetChatById.as_view()),
    path('create-new-chat/', CreateNewChat.as_view()),
    path('send-message/', SendMessage.as_view())
]