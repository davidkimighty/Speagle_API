from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


class User(AbstractUser):
    username = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(_('email address'), unique=True)
    # username and email is redifined, so that it overrides the existing username and email field
    # to set the unique parameter as True on email and blank parameters as True with username.  
    #date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)

    USERNAME_FIELD = 'email' # email field is used as a username for authentication.
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return "{}".format(self.email)

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    dob = models.DateField()
    country = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='uploads', blank=True) # ImageField requires pillow python package.