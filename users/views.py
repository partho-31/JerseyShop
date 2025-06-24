from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAdminUser
from django.http import HttpResponseRedirect 
from rest_framework.response import Response
from django.conf import settings as main_settings 
from sslcommerz_lib import SSLCOMMERZ
from django.db.models import Q,Sum
from django.utils import timezone
from datetime import timedelta
import uuid
from djoser.views import UserViewSet
from users.models import CustomUser,PaymentHistory
from orders.models import Order
from orders.serializers import CreateOrderSerializers



class CustomUserViewSet(UserViewSet):
    def get_queryset(self):
        return CustomUser.objects.select_related('cart')
        

@api_view(['POST'])
def PaymentInitiate(request):
    user = request.user
    amount = request.data.get('total_amount')


    settings = { 'store_id': 'homet681c8efac4942', 'store_pass': 'homet681c8efac4942@ssl', 'issandbox': True }
    sslcz = SSLCOMMERZ(settings)
    post_body = {}
    post_body['total_amount'] = amount
    post_body['currency'] = "BDT"
    post_body['tran_id'] = f'tnx_id:{uuid.uuid4().hex}'
    post_body['success_url'] = f'{main_settings.BACKEND_URL}/api/payment/success/'
    post_body['fail_url'] = f'{main_settings.BACKEND_URL}/api/payment/failed/'
    post_body['cancel_url'] = f'{main_settings.BACKEND_URL}/api/payment/cancel/'
    post_body['emi_option'] = 0
    post_body['cus_name'] = f'{user.first_name} {user.last_name}'
    post_body['cus_email'] = user.email
    post_body['cus_phone'] = user.phone_number
    post_body['cus_add1'] = user.address
    post_body['cus_city'] = "Dhaka"
    post_body['cus_country'] = "Bangladesh"
    post_body['shipping_method'] = "NO"
    post_body['multi_card_name'] = ""
    post_body['num_of_item'] = 1
    post_body['product_name'] = "Jersey"
    post_body['product_category'] = "Test Category"
    post_body['product_profile'] = "general"


    response = sslcz.createSession(post_body)

    if response.get('status') == 'SUCCESS':       
        PaymentHistory.objects.create(
            amount = post_body['total_amount'],
            tnx_id = post_body['tran_id'],
            user= user
        )
        return Response({'payment_url' : response.get('GatewayPageURL')})
    else:  
        return Response({'request' : 'Request failed!','response': response})


@api_view(['POST'])
def PaymentSuccess(request): 
    tnx_id = request.POST.get('tran_id')
    payment = PaymentHistory.objects.get(tnx_id=tnx_id)
    user = payment.user
    serializer = CreateOrderSerializers(data={}, user=user)
    serializer.is_valid(raise_exception=True)
    order = serializer.save()
    order.status = Order.PAID
    order.save()
    return HttpResponseRedirect(f'{main_settings.FRONTEND_URL}/payment/success/')


@api_view(['POST',])
def PaymentCancel(request):
    return HttpResponseRedirect(f'{main_settings.FRONTEND_URL}/payment/cancel/')  


@api_view(['POST',])
def PaymentFailed(request):
    return HttpResponseRedirect(f'{main_settings.FRONTEND_URL}/payment/failed/')


@api_view(['GET'])
@permission_classes([IsAdminUser])
def SalesReport(request):
    seven_days_ago = timezone.now() - timedelta(days=7)
    queryset = PaymentHistory.objects.aggregate(
            total_sales=Sum('amount'),
            weekly_sales=Sum('amount', filter=Q(created_at__gte=seven_days_ago))
        )
    return Response({'Sales_data' : queryset})
 