from django.urls import include, path, re_path

from .views import *


app_name = 'speagle'

urlpatterns = [
    re_path(r'^validate_email/', SendEmailForValidation.as_view()),
    re_path("^validate_key/$", ValidateKey.as_view()),
    re_path("^register/$", Register.as_view())
]