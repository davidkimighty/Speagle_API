from django.urls import path, include, reverse, re_path
from accounts.api.views import VerifyEmailAPI, VerifyValidationKeyAPI, RegisterAPI, UserRegistrationAPI, UserLoginAPI


urlpatterns = [
    path('verify_email/', VerifyEmailAPI.as_view(), name="verify_email"),
    path('verify_key/', VerifyValidationKeyAPI.as_view(), name="verify_key"),
    path('register/', UserRegistrationAPI.as_view(), name="register_user"),
    path('login/', UserLoginAPI.as_view(), name="login_user"),
]