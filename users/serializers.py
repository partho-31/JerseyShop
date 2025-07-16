from djoser.serializers import UserCreateSerializer,UserSerializer
from rest_framework import serializers
from djoser.serializers import PasswordResetConfirmSerializer


class CustomUserCreateSerializers(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        fields = ['first_name','last_name','email','password','phone_number','address']


class CustomUserSerializers(UserSerializer):
    cart = serializers.CharField()
    class Meta(UserSerializer.Meta):
        fields = '__all__'
        read_only_fields = ['password']



class CustomPasswordResetConfirmSerializer(PasswordResetConfirmSerializer):
    class Meta:
        ref_name = "DjoserPasswordResetConfirm"