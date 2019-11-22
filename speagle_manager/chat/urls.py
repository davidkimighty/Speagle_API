from django.conf.urls import url
from django.urls import path
from .views import index, room
from .views import load_inbox, load_messages, add_chatroom
app_name = 'chat'


urlpatterns = [
    path('', index, name='index'),
    path('<str:room_name>/', room, name='room'),

    path('load-inbox', load_inbox),
    path('load-messages', load_messages),
    path('add-chatroom', add_chatroom),
]