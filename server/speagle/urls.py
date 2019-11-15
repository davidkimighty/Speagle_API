from django.urls import path, include
from .views import user_index


urlpatterns = [
    path('api/auth/user_index', user_index.as_view()),
]