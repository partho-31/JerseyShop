from rest_framework.viewsets import ModelViewSet
from products.models import Category,Product,ProductImage,ProductReview
from products.serializers import ProductSerializers,CategorySerializers,ProductImageSerializers,ProductReviewSerializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.permissions import IsReviewAuthorOrReadOnly

class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializers
    queryset = Category.objects.prefetch_related('product').all()
    

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.prefetch_related('images').select_related('category').all()
    serializer_class = ProductSerializers


class ProductImageViewSet(ModelViewSet):
    serializer_class = ProductImageSerializers
    http_method_names = ["post", "delete"] 

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return ProductImage.objects.none()
        
        product_id = self.kwargs.get('product_pk')
        product = Product.objects.get(id=product_id)
        return  ProductImage.objects.filter(product= product)
    
    def perform_create(self, serializer):
        product_id = self.kwargs.get('product_pk')
        product = Product.objects.get(id=product_id)
        serializer.save(product=product)


class ProductReviewViewSet(ModelViewSet):
    serializer_class = ProductReviewSerializers
    permission_classes = [IsReviewAuthorOrReadOnly]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return ProductReview.objects.none()
        
        product_id = self.kwargs.get('product_pk')
        product = Product.objects.get(id=product_id)
        return ProductReview.objects.filter(product=product).select_related('user').all()

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

    def get_serializer_context(self):
        product_id = self.kwargs.get('product_pk')
        return {'product_id': product_id}
    

    
@api_view(['GET'])    
def LatestProduct(request):
    product = Product.objects.prefetch_related('images').select_related('category').latest()
    serializer = ProductSerializers(product)
    return Response(serializer.data)
