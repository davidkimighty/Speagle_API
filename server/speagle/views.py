from django.shortcuts import render, get_list_or_404

from rest_framework.views import APIView
from rest_framework.response import Response

import random
from .models import User
 

class SendEmailForValidation(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        
        if email:
            email = str(email)
            user = User.objects.filter(email__iexact = email)
            
            if user.exists():
                return Response({
                    'status' : False,
                    'detail' : 'This email is already in use'
                })
            else:
                key = send_mail(email)

                if key:
                    pass
                else:
                    return Response({
                        'status' : False,
                        'detail' : 'Sending mail error'
                    })
        else:
            return Response({
                'status' : False,
                'detail' : 'Email is needed for post request'
            })
    
def send_mail(email):
        if email:
            key = random.randint(999, 9999)
            return key
        else:
            return False