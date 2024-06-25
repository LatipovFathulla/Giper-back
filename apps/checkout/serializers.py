from rest_framework import serializers
from .models import Checkout
from apps.cart.serializers import CartItemSerializer


class CheckoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checkout
        fields = ['id', 'full_name', 'phone_number', 'region', 'town', 'address', 'comment', 'cart', 'user',
                  'PAY_STATUS',
                  'NAXT_STATUS', 'amount', 'created_at', 'generate_link']


class CheckoutAllSerializer(serializers.ModelSerializer):
    cart = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Checkout
        fields = ['id', 'full_name', 'phone_number', 'region', 'town', 'address', 'comment', 'cart', 'user',
                  'PAY_STATUS',
                  'NAXT_STATUS', 'created_at', 'amount', 'generate_link']
