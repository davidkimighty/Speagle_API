from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Room, Message
from channels.db import database_sync_to_async
import json

class ChatConsumer(AsyncWebsocketConsumer):
    def _is_authenticated(self):
        print(self.scope['user'])
        if hasattr(self.scope, 'auth_error'):
            return False
        if not self.scope['user'] or self.scope['user'] is 'AnonymousUser':
            return False
        return True

    
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        if self._is_authenticated():
            # print('consumer scope -> ' + str(self.scope))

            # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        if self._is_authenticated():
            text_data_json = json.loads(text_data)
            sender = str(self.scope['user']),
            message = text_data_json['message']
            print('message -> sender: ' + sender + message)

            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'sender': sender,
                    'message': message
                }
            )

    # Receive message from room group
    async def chat_message(self, event):
        sender = event['sender']
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'sender': sender,
            'message': message
        }))