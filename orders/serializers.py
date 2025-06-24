from rest_framework import serializers
from orders.models import Cart,CartItem,Order,OrderItem
from products.serializers import ProductSerializers
from users.serializers import CustomUserSerializers



class CartSerializers(serializers.ModelSerializer):
    total_amount = serializers.SerializerMethodField(method_name='get_total')
    total_items = serializers.SerializerMethodField(method_name='get_total_items')
    class Meta:
        model = Cart
        fields = ['id','user','total_amount','created_at','total_items']
        read_only_fields = ['id','created_at','total_amount','user','total_items']

    def get_total(self,obj):
        return sum([item.product.price*item.quantity for item in obj.cartItem.all()])
    
    def get_total_items(self,obj):
        return obj.cartItem.count()


class CartItemSerializers(serializers.ModelSerializer):
    product = ProductSerializers()
    total_cost = serializers.SerializerMethodField(method_name= 'total')
    class Meta:
        model = CartItem
        fields = ['id','product','quantity','cart','total_cost']
        read_only_fields = ['id']

    def total(self,obj):
        return obj.product.price * obj.quantity


class addCartItemSerializers(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['product','quantity']
        
    def create(self, validated_data):
        cart =  self.context.get('cart')
        product = validated_data.get('product')
        quantity = validated_data.get('quantity')

        cartItem,created = CartItem.objects.get_or_create(cart=cart, product=product)
        if created:
            cartItem.quantity = quantity
        else:
            cartItem.quantity += quantity
        cartItem.save()
        return cartItem
 



class CreateOrderSerializers(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  
        super().__init__(*args, **kwargs)

    def create(self, validated_data):
        user = self.user  
        try:
            cart = user.cart
        except Cart.DoesNotExist:
            raise serializers.ValidationError("Cart does not exist.")

        order = Order.objects.create(user=user)
        order_items = [
            OrderItem(order=order, product=item.product, quantity=item.quantity)
            for item in cart.cartItem.all()
        ]
        OrderItem.objects.bulk_create(order_items)
        cart.delete()
        return order

    def to_representation(self, instance):
        return OrderSerializers(instance).data



class UpdateOrderSerializers(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']



class OrderItemSerializers(serializers.ModelSerializer):
    product = ProductSerializers()
    total_cost = serializers.SerializerMethodField(method_name='get_total_cost')
    class Meta:
        model = OrderItem
        fields = ['id','product','quantity','total_cost']

    def get_total_cost(self,obj):
        return obj.product.price * obj.quantity
    

class OrderSerializers(serializers.ModelSerializer):
    user = CustomUserSerializers()
    orderItem = OrderItemSerializers(many= True,read_only=True)
    total_amount = serializers.SerializerMethodField(method_name='get_total')
    class Meta:
        model = Order
        fields = ['id','status','created_at','user','orderItem','total_amount']
        read_only_fields = ['id','status','total_amount','created_at','user','orderItem']

    def get_total(self,obj):
        return sum([item.product.price*item.quantity for item in obj.orderItem.all()])


   
    

