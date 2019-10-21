from .models import User
from rest_framework import viewsets, permissions
from .serializers import SpeagleSerializer

#Speagle Viewset
class SpeagleViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [
         permissions.AllowAny
    ]
    serializer_class = SpeagleSerializer