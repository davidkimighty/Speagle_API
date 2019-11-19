from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
# from django.core.validators import validate_email
# from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _

from accounts.models import User

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password')
        read_only_fields = ['id']

# AbstractBaseUser Register Serializer
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

# AbstractUser Register Serializer
class AbstractUserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True,validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(min_length=4, max_length=100, write_only=True)
    confirm_password = serializers.CharField(min_length=4, max_length=100, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'confirm_password', 'date_joined')

    # def create(self, validated_data):
    #     password = validated_data.pop('password')
    #     user = User(**validated_data)
    #     user.set_password(password)
    #     user.save()
    #     return user

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            password=make_password(validated_data['password'])
        )
        return user

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('confirm_password'):
            raise serializers.ValidationError("Passwords don't match.")
        return attrs

# AbstractUser Login Serializer
class AbstractUserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})

    # Email validation needed
    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            if User.objects.filter(email = email).exists():
                user = authenticate(
                    request = self.context.get('request'),
                    username = email,
                    password = password,
                )
        data['user'] = user
        return data