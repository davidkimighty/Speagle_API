from django.urls import include, path, re_path

from .views import SendEmailForValidation


app_name = 'speagle'

urlpatterns = [
    re_path(r'^validate_email/', SendEmailForValidation.as_view())
]