from django.urls import path
from .views import *


urlpatterns = [
    path('get-user-chats-by-id/<str:user_id>/', GetUserChatsById.as_view()),
    path('get-chat-by-name/<str:name>/', GetChatByName.as_view()),
    path('get-chat-by-id/<int:id>/', GetChatById.as_view()),
    path('create-new-chat/', CreateNewChat.as_view()),
    path('send-message/', SendMessage.as_view())
]