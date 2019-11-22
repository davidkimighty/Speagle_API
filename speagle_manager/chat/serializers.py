from rest_framework import serializers

from .models import ChatRoom, Message, UnreadMessages


class MessageSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='hash_id', read_only=True)
    sender_id = serializers.CharField(source='sender.hash_id', read_only=True)
    sender_email = serializers.EmailField(source='sender.email', read_only=True)
    thread_id = serializers.CharField(source='thread.hash_id', read_only=True)
                             
    class Meta:
        model = Message
        fields = ('id','sent','text','sender_id','sender_email','thread_id')
                             
                             
class MessageListSerializer(serializers.ListSerializer):
    child = MessageSerializer()
    many = True
    allow_null = True


class ThreadSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='hash_id',read_only=True)
    unread_count = serializers.IntegerField(read_only=True)
    last_message = MessageSerializer(read_only=True,many=False)
    title = serializers.CharField(default="speagle",read_only=True)
                             
    class Meta:
        model = ChatRoom
        fields = ('id','title','last_message','unread_count')
                             
                             
class ThreadListSerializer(serializers.ListSerializer):
    child = ThreadSerializer()
    many = True
    allow_null = True