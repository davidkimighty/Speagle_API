from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.http import JsonResponse, HttpResponse
from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, permissions, status
from rest_framework.response import Response
import json
                             
from .models import MessageThread, Message, Unreads
from .serializers import MessageSerializer, MessageListSerializer, ThreadSerializer, ThreadListSerializer


def index(request):
    return render(request, 'chat/index.html', {})

def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })

