from django.contrib import admin
from orders.models import Cart,CartItem,Order,OrderItem



class CustomCart(admin.ModelAdmin):
    model = Cart
    list_display = ('id','user')

admin.site.register(Cart,CustomCart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
