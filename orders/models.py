from django.db import models
from django.core.validators import MinValueValidator
from users.models import CustomUser
from products.models import Product
import uuid



class Cart(models.Model):
    id = models.UUIDField(primary_key= True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='cart')

    def __str__(self):
        return f"Cart of {self.user.get_full_name()}"


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cartItem')
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)],default=1)

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cartItem')

    class Meta:
        unique_together = [['product','cart']]

    def __str__(self):
        return f"{self.quantity} x {self.product}"
    

class Order(models.Model):
    PAID = 'Paid'
    NOT_PAID = 'Not Paid'
    SHIPPED = 'Shipped'
    DELIVERED = 'Delivered'
    CANCELED = 'Canceled'
    STATUS_CHOICES = [
        (PAID, 'Paid'),
        (NOT_PAID, 'Not Paid'),
        (SHIPPED, 'Shipped'),
        (DELIVERED, 'Delivered'),
        (CANCELED, 'Canceled')
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4,editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default= NOT_PAID)

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='order')

    def __str__(self):
        return f"Order {self.id} by {self.user.first_name} - {self.status}"


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order')
    quantity = models.IntegerField()

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orderItem')

    def __str__(self):
        return f"{self.product} x {self.quantity}"
    
