from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import CartItem
from ..products.models import NewProductModel, NewMedia
from django.forms.models import model_to_dict
from ..products.serializers import NewProductSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'phone_number', 'created_at', 'is_staff', 'is_active']


class DashUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'phone_number', 'first_name', 'created_at', 'is_staff', 'is_active']


class CartItemSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    product = NewProductSerializer()

    class Meta:
        model = CartItem
        fields = ('id', 'user', 'product', 'quantity', 'total', 'cart_status', 'created_at', 'updated_at')


class CartCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ('id', 'user', 'product', 'quantity', 'total', 'cart_status', 'created_at', 'updated_at')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        us = User.objects.get(id=data['user'])
        pr = NewProductModel.objects.get(id=data['product'])
        media = NewMedia.objects.filter(product=data['product'])
        if media.exists():
            request = self.context.get('request')
            host = request.get_host() if request else 'localhost'
            media_urls = [f"http://{host}{m.img_url.url}" for m in media]
        else:
            media_urls = 'не найден'
        serialized_obj = model_to_dict(pr, exclude=['created_at', 'updated_at', 'weight', 'attribute_values'])
        serialized_obj['brand'] = [model_to_dict(brand) for brand in pr.brand.all()]
        serialized_obj['color'] = [model_to_dict(color) for color in pr.color.all()]
        serialized_obj2 = model_to_dict(us)
        data['media'] = media_urls
        data['product'] = serialized_obj
        data['user'] = serialized_obj2
        return data
