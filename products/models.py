from django.db import models
from cloudinary.models import CloudinaryField
from django.core.validators import MinValueValidator,MaxValueValidator
from users.models import CustomUser


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    total_product = models.PositiveIntegerField(validators=[MinValueValidator(0)], blank=True, null=True)
    image = CloudinaryField('image')


    def __str__(self):
        return self.name
    

class Product(models.Model):
    name = models.CharField(max_length=150, blank=False)
    price = models.DecimalField(max_digits=10, decimal_places=2,validators=[MinValueValidator(0)])
    discount = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0),MaxValueValidator(100)])
    stock = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product')
    description = models.TextField()
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        get_latest_by = 'created_at'

    def __str__(self):
        return self.name
    

class ProductImage(models.Model):
    image = CloudinaryField('image')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return self.product.name


class ProductReview(models.Model):
    rating = models.PositiveIntegerField(validators=[MinValueValidator(0),MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = CloudinaryField('image',blank=True,null=True)


    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reviews')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')

    def __str__(self):
        return self.comment