from rest_framework import serializers
from products.models import Product,ProductImage,Category,ProductReview
from users.serializers import CustomUserSerializers
from django.db.models import Avg
from decimal import Decimal
from users.models import CustomUser



class CategorySerializers(serializers.ModelSerializer):
    total_product = serializers.SerializerMethodField('get_total_product')
    image = serializers.ImageField()
    class Meta:
        model = Category
        fields = ['id','name','total_product','description','image']
        read_only_fields = ['id','total_product']

    def get_total_product(self,obj):
        return obj.product.count()


class ImageSerializers(serializers.ModelSerializer):
    image = serializers.ImageField()
    class Meta:
        model = ProductImage
        fields = ['id','image']
        read_only_fields = ['id']


class ReviewUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "image"]


class ProductReviewSerializers(serializers.ModelSerializer):
    user = ReviewUserSerializer()
    image = serializers.ImageField(required=False, allow_null=True)
    class Meta:
        model = ProductReview
        fields = ['id','rating','comment','user','image']
        read_only_fields = ['id','user']

    def create(self, validated_data):
        id = self.context.get('product_id')
        # product = Product.objects.get(id=id)
        return ProductReview.objects.create(product_id=id,**validated_data)


class CreateProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name','price','discount','stock','category','description']
        
    def validate_price(self,price):
        if price <= 0:
            raise serializers.ValidationError('Price must be greater than 0')
        return price
    

class ProductSerializers(serializers.ModelSerializer):
    images = ImageSerializers(many=True, read_only=True)
    final_price = serializers.SerializerMethodField()
    ratings = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    remaining = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id','name','price','discount','stock','description','created_at','category','ratings','final_price','remaining','images']

    def get_category(self,obj):
        return obj.category.name

    def get_final_price(self,obj):
        return obj.price - (obj.price*( Decimal(obj.discount)/100))

    def get_ratings(self,obj):
        return obj.avg_rating
    
    def get_remaining(self,obj):
        return obj.stock - (obj.ordered_quantity or 0)
    

class ProductImageSerializers(serializers.ModelSerializer):
    image = serializers.ImageField()
    class Meta:
        model = ProductImage
        fields = ['image']




    

