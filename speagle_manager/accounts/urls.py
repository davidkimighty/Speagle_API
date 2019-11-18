from django.urls import path, include, reverse, re_path
from rest_framework.authtoken import views
from rest_framework_expiring_authtoken import views
from accounts.api.views import RegisterAPI, UserRegistrationAPIView, UserLoginAPIView


urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name="register_user"),
    path('login/', UserLoginAPIView.as_view(), name="login_user"),
    # re_path(r'^login/', views.obtain_auth_token),
    # re_path(r'^login/', views.obtain_expiring_auth_token),
]
