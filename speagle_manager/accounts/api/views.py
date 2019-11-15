from django.http import Http404
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.models import User
from accounts.serializers import (
    UserSerializer, RegisterSerializer, LoginSerializer, AbstractUserRegisterSerializer
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


# Login API
# class LoginAPI(generics.GenericAPIView):
#     serializer_class = LoginSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         if login(request, user):
#             return Response({
#                 "user": UserSerializer(user, context=self.get_serializer_context()).data,
#             })