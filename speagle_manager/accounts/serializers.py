from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email')

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

        def create(self, validated_data):
            user = User.objects.create_user(
                validated_data['email'],
                validated_data['password']
            )
            return user

# Login Serializer
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style = {'input_type': 'password'},
        trim_whitespace = False,
    )

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            if User.objects.filter(email = email).exists():
                user = authenticate(
                    # request = self.context.get('request'),
                    username = email,
                    password = password,
                )
                print(user)

        data['user'] = user
        return data