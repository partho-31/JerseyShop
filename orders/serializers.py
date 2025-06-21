from rest_framework import serializers
from orders.models import Cart,CartItem,Order,OrderItem
from products.serializers import ProductSerializers
from users.serializers import CustomUserSerializers



class CartSerializers(serializers.ModelSerializer):
    total_amount = serializers.SerializerMethodField(method_name='get_total')
    class Meta:
        model = Cart
        fields = ['id','user','total_amount','created_at']
        read_only_fields = ['id','created_at','total_amount','user']

    def get_total(self,obj):
        return sum([item.product.price*item.quantity for item in obj.cartItem.all()])


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
 

class OrderSerializers(serializers.ModelSerializer):
    user = CustomUserSerializers()
    total_amount = serializers.SerializerMethodField(method_name='get_total')
    class Meta:
        model = Order
        fields = ['id','status','created_at','user','total_amount']
        read_only_fields = ['id','status','total_amount','created_at','user']

    def get_total(self,obj):
        return sum([item.product.price*item.quantity for item in obj.orderItem.all()])


           
class CreateOrderSerializers(serializers.Serializer):
    class Meta:
        model = Order
        fields =  ['user']

    def create(self, validated_data):
        user = validated_data.get('user')
        try:
            cart = user.cart
        except Cart.DoesNotExist:
            raise serializers.ValidationError("Cart does not exist.")
        
        order = Order.objects.create(user=user)
        orderItem = [ OrderItem(
                order=order,
                product=item.product,
                quantity=item.quantity
        )
        for item in cart.cartItem.all()]
        OrderItem.objects.bulk_create(orderItem)
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
    


   
    

