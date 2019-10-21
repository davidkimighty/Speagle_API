from rest_framework import serializers
from .models import User

#Speagle Serializer
class SpeagleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'