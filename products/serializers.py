from rest_framework import serializers
from products.models import Product,ProductImage,Category,ProductReview
from users.serializers import CustomUserSerializers


class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name','total_product','description']
        read_only_fields = ['id','total_product']


class ImageSerializers(serializers.ModelSerializer):
    image = serializers.ImageField()
    class Meta:
        model = ProductImage
        fields = ['id','image']
        read_only_fields = ['id']


class ProductSerializers(serializers.ModelSerializer):
    images = ImageSerializers(many=True, read_only=True)
    class Meta:
        model = Product
        fields = ['id','name','price','discount','stock','category','description','images']
        read_only_fields = ['id']

    def validate_price(self,price):
        if price <= 0:
            raise serializers.ValidationError('Price must be greater than 0')
        return price


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
    

