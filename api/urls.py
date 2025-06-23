from django.urls import path,include
from rest_framework_nested import routers

from products.views import ProductViewSet,CategoryViewSet,ProductImageViewSet,ProductReviewViewSet,LatestProduct
from orders.views import CartViewSet,CartItemViewSet,OrderViewSet,OrderItemViewSet,OrderOverview
from users.views import PaymentInitiate,PaymentSuccess,PaymentCancel,PaymentFailed

router = routers.SimpleRouter()
router.register('products',ProductViewSet, basename='product')
router.register('category',CategoryViewSet, basename='category')
router.register('cart',CartViewSet, basename='cart')
router.register('order',OrderViewSet,basename='order')

product_router = routers.NestedSimpleRouter(router,'products',lookup='product')
product_router.register('images',ProductImageViewSet,basename='product-image')

review_router = routers.NestedSimpleRouter(router,'products',lookup='product')
review_router.register('review',ProductReviewViewSet,basename='product-review')

cartItem_router = routers.NestedDefaultRouter(router,'cart',lookup='cart')
cartItem_router.register('items',CartItemViewSet,basename='cart-item')

orderItem_router = routers.NestedDefaultRouter(router,'order',lookup='order')
orderItem_router.register('items',OrderItemViewSet,basename='order-item')

urlpatterns = [
    path('',include(router.urls)),
    path('',include(product_router.urls)),
    path('',include(review_router.urls)),
    path('',include(cartItem_router.urls)),
    path('',include(orderItem_router.urls)),
    path('latest/products/',LatestProduct, name='latestProduct'),
    path('orders/overview/',OrderOverview, name='orderOverview'),
    path('payment/initiate/',PaymentInitiate, name='payment-initiate'),
    path('payment/success/',PaymentSuccess, name='payment-success'),
    path('payment/cancel/',PaymentCancel, name='payment-cancel'),
    path('payment/failed/',PaymentFailed, name='payment-failed'),
]
