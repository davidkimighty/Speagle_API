from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.conf import settings


GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

class UserManager(BaseUserManager):
    def _create_user(self, email, password=None, is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError('email must be set')
        if not password:
            raise ValueError('password must be set')

        user_obj = self.model(email=self.normalize_email(email))
        user_obj.set_password(password)
        user_obj.active = is_active
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.save(using=self._db)
        return user_obj

    def create_user(self, email, password=None):
        user = self._create_user(
            email,
            password=password,
            is_staff=True,
        )
        return user

    def create_superuser(self, email, password=None):
        user = self._create_user(
            email,
            password=password,
            is_staff=True,
            is_admin=True,
        )
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email'), unique=True)
    active = models.BooleanField(_('active'), default=True)
    staff = models.BooleanField(_('staff'), default=False)
    admin = models.BooleanField(_('admin'), default=False)
    # is_superuser = models.BooleanField(_('superuser'), default=False)

    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    last_login = models.DateTimeField(_('last login'), auto_now=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    gender = models.CharField(_('gender'), max_length=1, choices=GENDER_CHOICES, blank=True)
    dob = models.DateField(_('date of birth'), null=True, blank=True)
    country = models.CharField(_('country'), max_length=50, blank=True)
    photo = models.ImageField(upload_to='uploads', null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def has_perm(self, perm, obj=None):
        # return super().has_perm(perm, obj=obj)
        return True

    def has_module_perms(self, app_label):
        # return super().has_module_perms(app_label)
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active

# class UserProfile(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
#     username = models.CharField(_('username'), max_length=10, blank=True)
#     first_name = models.CharField(_('first name'), max_length=30, blank=True)
#     last_name = models.CharField(_('last name'), max_length=30, blank=True)
#     gender = models.CharField(_('gender'), max_length=1, choices=GENDER_CHOICES, blank=True)
#     dob = models.DateField(_('date of birth'), blank=True)
#     country = models.CharField(_('country'),max_length=50)
#     photo = models.ImageField(upload_to='uploads', null=True, blank=True)

class EmailKey(models.Model):
    email = models.EmailField(_('email'), unique=True)
    key = models.CharField(_("key"), max_length=9, blank=True, null=True)
    count = models.IntegerField(_("count"), default=0)
    validated = models.BooleanField(_("validated"), default=False)

    def __str__(self):
        return str(self.email) + ' key : ' + str(self.key)