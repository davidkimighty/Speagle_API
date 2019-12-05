from rest_framework import serializers
                             
from .models import MessageThread, Message, Unreads


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.CharField(source='sender.email', read_only=True)
    thread = serializers.CharField(source='thread.title', read_only=True)

    class Meta:
        model = Message
        fields = ('id', 'timestamp', 'text', 'sender', 'thread')

    def create(self, validated_data):
        sender = self.context['request'].user
        msg = Message(
            sender=sender,
            text=validated_data['text'],
            # thread=
        )

class MessageListSerializer(serializers.ListSerializer):
    child = MessageSerializer()
    many = True
    allow_null = True


class ThreadSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='title', read_only=True)
    unread = MessageSerializer(read_only=True, many=False)
    unread_count = serializers.CharField(read_only=True)

    class Meta:
        model = MessageThread
        fields = ('id', 'unread', 'unread_count')


class ThreadListSerializer(serializers.ListSerializer):
    child = ThreadSerializer()
    many = True
    allow_null = True