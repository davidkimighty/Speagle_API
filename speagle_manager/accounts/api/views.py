from django.urls import reverse
from rest_framework import generics, permissions, status
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from accounts.models import User, ValidationKey
from .serializers import UserSerializer, RegisterSerializer, AbstractUserRegisterSerializer, AbstractUserLoginSerializer
import random

# Verify email and send validation key
class VerifyEmailAPI(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        raw_email = request.data.get('email')

        if raw_email:
            email = str(raw_email)
            user = User.objects.filter(email__iexact = email)

            if user.exists():
                return Response({
                    'status': False,
                    'details': 'This eamil already exists.'
                })
            else:
                new_key = create_key(email)
                if new_key:
                    send_mail(email, new_key)
                    key = ValidationKey.objects.filter(email__iexact=email)

                    if key.exists():
                        key = key.first()
                        count = key.count

                        if count > 6:
                            return Response({
                                'status': False,
                                'details': 'Reached limitation.'
                            })
                        key.count = count + 1
                        key.save()
                        return Response({
                            'status': True,
                            'details': 'Validation key successfully sent.'
                        })
                    else:
                        ValidationKey.objects.create(email=email, key=new_key) 
                        return Response({
                            'status': True,
                            'details': 'Validation key successfully sent.'
                        })
                else:
                    return Response({
                        'status': False,
                        'details': 'Failed to send validation key.'
                    })
        else:
            return Response({
                'status': False,
                'details': 'This eamil already exists.'
            })

# Create validation key
def create_key(email):
    if email:
        key = random.randint(999, 9999)
        print(key)
        return key
    else:
        return False

# Send validation key through email 
def send_mail(email, new_key):
    if email:
        # smtp needed
        print(email)

# Verify validation key
class VerifyValidationKeyAPI(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        email = request.data.get('email', False)
        raw_key = request.data.get('key', False)

        if email and raw_key:
            old_key = ValidationKey.objects.filter(email__iexact = email)
            
            if old_key.exists():
                old_key = old_key.first()
                key = old_key.key

                if str(raw_key) == str(key):
                    old_key.validated = True
                    old_key.save() # Why save the old one.
                    return Response({
                        'status': True,
                        'details': 'Correct validation key.'
                    })
                else:
                    return Response({
                        'status': False,
                        'details': 'Incorrect validation key.'
                    })
            else:
                return Response({
                    'status': False,
                    'details': 'Request validation key first.'
                })
        else:
            return Response({
                'status': False,
                'details': 'Email & validation key must be set.'
            })

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
class UserRegistrationAPI(CreateAPIView):
    authentication_classes = ()
    permission_classes = (permissions.AllowAny,)
    serializer_class = AbstractUserRegisterSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email', False)
        password = request.data.get('password', False)

        if email and password:
            old = ValidationKey.objects.filter(email__iexact = email)
            
            if old.exists():
                old = old.first()
                validated = old.validated
                
                if validated:
                    serializer = self.get_serializer(data=request.data)
                    serializer.is_valid(raise_exception=True)
                    self.perform_create(serializer)
                    user = serializer.instance
                    token, created = Token.objects.get_or_create(user=user)

                    data = serializer.data
                    data["token"] = token.key
                    headers = self.get_success_headers(serializer.data)
                    old.delete()
                    # return Response(data, status=status.HTTP_201_CREATED, headers=headers)
                    return Response({
                        'status': True,
                        'details': 'Account created'
                    })
                else:
                    return Response({
                        'status': False,
                        'details': 'Verification of validation key is needed.'
                    })
            else:
                return Response({
                    'status': False,
                    'details': 'Email validation is needed.'
                })
        else:
            return Response({
                'status': False,
                'details': 'Email & password must be set.'
            })

# Login API
class UserLoginAPI(generics.GenericAPIView):
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