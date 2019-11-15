from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'is_staff', 'is_superuser')
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, data):
        instance = User.objects.create(
            email=data.get('email'),
            is_staff=data.get('is_staff'),
            is_superuser=data.get('is_superuser'),
        )
        instance.set_password(data.get('password'))
        instance.save()
        return instance

    def update(self, instance, data):
        instance.email = data.get('email', instance.email)
        instance.is_staff = data.get('is_staff', instance.is_staff)
        instance.is_superuser = data.get('is_superuser', instance.is_staff)
        instance.set_password(data.get('password'))
        instance.save()
        return instance