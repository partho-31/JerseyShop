from django.shortcuts import render
from djoser.views import UserViewSet
from users.models import CustomUser



class CustomUserViewSet(UserViewSet):
    def get_queryset(self):
        return CustomUser.objects.select_related('cart')
