from django.db import models

# Create your models here.
class User(models.Model):
    userId = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    createdAt = models.DateTimeField(auto_now_add=True)
    # GENDER_CHOICES = (
    #     ('M', 'Male'),
    #     ('F', 'Female'),
    # )
    # gender = models.CharField(max_length=1, choices=GENDER_CHOICES)