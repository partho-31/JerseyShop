from django.db import models
from django.core.validators import MinValueValidator
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
    

class Contact(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField(blank=False, null=False)
    phone = models.CharField(max_length=15, blank=False, null=False)
    message = models.TextField(blank=False, null=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
    

class PaymentHistory(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2,validators=[MinValueValidator(0)])
    tnx_id = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="payment")

    def __str__(self):
        return self.tnx_id