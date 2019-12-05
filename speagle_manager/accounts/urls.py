from django.urls import path, include, reverse, re_path
from .views import (
    VerifyEmailAPI,
    VerifyValidationKeyAPI,
    TokenRegistrationAPI,
    TokenLoginAPI,
    TokenLogoutAPI,
    RegisterAPI,
    JWTLoginAPI,
    SessionLoginAPI,
    SessionLogoutAPI
)


urlpatterns = [
    path('verify-email/', VerifyEmailAPI.as_view(), name="verify_email"),
    path('verify-key/', VerifyValidationKeyAPI.as_view(), name="verify_key"),
    path('token-register/', TokenRegistrationAPI.as_view(), name="token_register"),
    path('token-login/', TokenLoginAPI.as_view(), name="token_login"),
    path('token-logout/', TokenLogoutAPI.as_view(), name="token_logout"),
    path('register/', RegisterAPI.as_view(), name="register"),
    path('jwt-login/', JWTLoginAPI.as_view(), name="jwt_login"),
    path('session-login/', SessionLoginAPI.as_view(), name="session_login"),
    path('session-logout/', SessionLogoutAPI.as_view(), name="session_logout"),
    
]