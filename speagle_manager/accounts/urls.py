from django.urls import path, include
from accounts.api.views import RegisterAPI


urlpatterns = [
    path('api/auth/register', RegisterAPI.as_view()),
    # path('api/auth/login', LoginAPI.as_view()),
]
