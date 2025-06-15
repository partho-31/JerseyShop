from rest_framework import serializers
from products.models import Product,ProductImage,Category,ProductReview
from users.serializers import CustomUserSerializers
from django.db.models import Avg
from decimal import Decimal


class CategorySerializers(serializers.ModelSerializer):
    total_product = serializers.SerializerMethodField('get_total_product')
    class Meta:
        model = Category
        fields = ['id','name','total_product','description']
        read_only_fields = ['id','total_product']

    def get_total_product(self,obj):
        return obj.product.count()


class ImageSerializers(serializers.ModelSerializer):
    image = serializers.ImageField()
    class Meta:
        model = ProductImage
        fields = ['id','image']
        read_only_fields = ['id']


class ProductSerializers(serializers.ModelSerializer):
    images = ImageSerializers(many=True, read_only=True)
    final_price = serializers.SerializerMethodField('get_final_price')
    ratings = serializers.SerializerMethodField('get_ratings')

    class Meta:
        model = Product
        fields = ['id','name','price','discount','stock','category','description','images','final_price','ratings']
        read_only_fields = ['id','final_price','ratings']

    def validate_price(self,price):
        if price <= 0:
            raise serializers.ValidationError('Price must be greater than 0')
        return price

    def get_final_price(self,obj):
        return obj.price - (obj.price*( Decimal(obj.discount)/100))

    def get_ratings(self,obj):
        result = obj.reviews.aggregate(avg_rating=Avg('rating'))
        average = result['avg_rating']
        return round(average) if average is not None else 0
        

class ProductImageSerializers(serializers.ModelSerializer):
    image = serializers.ImageField()
    class Meta:
        model = ProductImage
        fields = ['product','image']



class ProductReviewSerializers(serializers.ModelSerializer):
    user = CustomUserSerializers(read_only=True)
    class Meta:
        model = ProductReview
        fields = ['id','rating','comment','user']
        read_only_fields = ['id','user']

    def create(self, validated_data):
        id = self.context.get('product_id')
        product = Product.objects.get(id=id)
        return ProductReview.objects.create(product=product,**validated_data)
    

