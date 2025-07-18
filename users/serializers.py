from djoser.serializers import UserCreateSerializer,UserSerializer
from rest_framework import serializers



class CustomUserCreateSerializers(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        fields = ['first_name','last_name','email','password','phone_number','address']


class CustomUserSerializers(UserSerializer):
    cart = serializers.CharField()
    class Meta(UserSerializer.Meta):
        fields = '__all__'
        read_only_fields = ['password']

