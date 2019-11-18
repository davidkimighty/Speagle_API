from django.urls import reverse
from rest_framework import generics, permissions, status
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from accounts.models import User
from .serializers import (
    UserSerializer, RegisterSerializer, AbstractUserRegisterSerializer, AbstractUserLoginSerializer,
)

# Register API
class RegisterAPI(generics.GenericAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = AbstractUserRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({'user': UserSerializer(user, context=self.get_serializer_context()).data, })

# Register API with token
class UserRegistrationAPIView(CreateAPIView):
    authentication_classes = ()
    permission_classes = (permissions.AllowAny,)
    serializer_class = AbstractUserRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        user = serializer.instance
        token, created = Token.objects.get_or_create(user=user)

        data = serializer.data
        data["token"] = token.key
        headers = self.get_success_headers(serializer.data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

# Login API
class UserLoginAPIView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = AbstractUserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        content = {
            'token': token.key,
        }
        return Response(content)