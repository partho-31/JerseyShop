from django.db import models
from django.contrib.auth.models import AbstractUser
from users.managers import CustomManagerUser
from cloudinary.models import CloudinaryField


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    image = CloudinaryField('image',default="default_j9jrqh", blank=True,null=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomManagerUser()

    def __str__(self):
        return self.email

