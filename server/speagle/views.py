from django.shortcuts import render, get_list_or_404

from rest_framework.views import APIView
from rest_framework.response import Response

import random
from .models import User, EmailKey
from .tokens import account_activation_token
 

class SendEmailForValidation(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        
        if email:
            email = str(email)
            user = User.objects.filter(email__iexact = email)
            
            if user.exists():
                return Response({
                    'status' : False,
                    'detail' : 'This email is already in use.'
                })
            else:
                key = generate_key(email)
                if key:
                    old = EmailKey.objects.filter(email__iexact = email)
                    if old.exists():
                        old = old.first()
                        count = old.count
                        if count > 6:
                            return Response({
                                'status' : False,
                                'detail' : 'Sending mail error. Limitation exceeded.'
                            })
                        old.count = count + 1
                        old.save()
                        print("count: ", count)
                        return Response({
                            'status' : True,
                            'detail' : 'Key is successfully sent.'
                        })
                    else:
                        EmailKey.objects.create(email=email, key=key)
                        return Response({
                            'status' : True,
                            'detail' : 'Key is successfully sent.'
                        })
                else:
                    return Response({
                        'status' : False,
                        'detail' : 'Sending mail error.'
                    })
        else:
            return Response({
                'status' : False,
                'detail' : 'Email is needed for post request.'
            })
    
def generate_key(email):
        if email:
            key = random.randint(999, 9999)
            print(key)
            # key = account_activation_token.make_token(user)
            return key
        else:
            return False


class ValidateKey(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email', False)
        key_sent = request.data.get('key', False)

        if email & key_sent:
            old = EmailKey.objects.filter(email__iexact = email)
            if old.exists():
                old = old.first()
                key = old.key
                if str(key_sent) == str(key):
                    old.validated = True
                    old.save()
                    return Response({
                        'status' : True,
                        'detail' : 'Key matched.'
                    })
                else:
                    return Response({
                        'status' : False,
                        'detail' : 'Incorrect key.'
                    })
            else:
                return Response({
                    'status' : False,
                    'detail' : 'Send key first to validate.'
                })
        else:
            return Response({
                'status' : False,
                'detail' : 'Both email and key is needed for validation.'
            })