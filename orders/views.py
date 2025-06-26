from rest_framework.mixins import CreateModelMixin,DestroyModelMixin,RetrieveModelMixin,UpdateModelMixin,ListModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.viewsets import ModelViewSet
from orders.serializers import CartSerializers,CartItemSerializers,addCartItemSerializers,OrderSerializers,UpdateOrderSerializers,OrderItemSerializers
from orders.models import Cart,CartItem,Order,OrderItem
from rest_framework.decorators import action,api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count,Q


class CartViewSet(CreateModelMixin,
                  RetrieveModelMixin,
                  UpdateModelMixin,
                  DestroyModelMixin,
                  GenericViewSet):
    serializer_class = CartSerializers
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Cart.objects.filter(user = self.request.user)
        else:
            return Cart.objects.none()
    
    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

    def create(self, request, *args, **kwargs):
        try:    
            existing_cart = Cart.objects.get(user = self.request.user)
            serializer = self.get_serializer(existing_cart)
            return Response(serializer.data,status= status.HTTP_200_OK)
        except Cart.DoesNotExist:
            return super().create(request, *args, **kwargs)



class CartItemViewSet(ModelViewSet):
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return addCartItemSerializers
        return CartItemSerializers

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Cart.objects.none()
        
        cart, created = Cart.objects.get_or_create(user=user)
        return CartItem.objects.filter(cart=cart)
 
    def perform_create(self, serializer):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        serializer.context['cart'] = cart
        serializer.save()



class OrderViewSet(ListModelMixin,
                  RetrieveModelMixin,
                  UpdateModelMixin,
                  DestroyModelMixin,
                  GenericViewSet):
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Order.objects.none()
        base_queryset = Order.objects.prefetch_related('orderItem').select_related('user').order_by('-created_at')
        if self.request.user.is_staff:
            return base_queryset
        return base_queryset.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UpdateOrderSerializers
        return OrderSerializers


    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        order = self.get_object()
        user = self.request.user

        if order.status == Order.DELIVERED:
            raise ValidationError({"detail": "You cannot cancel a delivered order."})

        if user.is_staff or order.user == user:
            order.status = Order.CANCELED
            order.save()
            serializer = self.get_serializer(order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(
            {"detail": "You do not have permission to cancel this order."},
            status=status.HTTP_403_FORBIDDEN
        )
    
    @action(detail=True, methods=['patch'])
    def update_status(self,request,pk=None):
        order = self.get_object()
        serializer = UpdateOrderSerializers(order,data= request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)



class OrderItemViewSet(ModelViewSet):
    serializer_class = OrderItemSerializers
    
    def get_queryset(self):
        orderId = self.kwargs.get('order_pk')
        return OrderItem.objects.filter(order_id=orderId)
    

@api_view(['GET'])
def OrderOverview(request):
    overview = Order.objects.aggregate(
        total=Count('id'),
        paid=Count('id', filter=Q(status=Order.PAID)),
        not_paid=Count('id', filter=Q(status=Order.NOT_PAID)),
        shipped=Count('id', filter=Q(status=Order.SHIPPED)),
        delivered=Count('id', filter=Q(status=Order.DELIVERED)),
        canceled=Count('id', filter=Q(status=Order.CANCELED)),
    )
    return Response({'order_overview' : overview})
    