from django.contrib.auth import get_user_model
from django.forms import model_to_dict
from rest_framework import serializers
from .models import Slider, Stock, Brand, Add_to_wishlist
from ..cart.serializers import UserSerializer
from ..products.models import NewProductModel, NewMedia
from ..products.serializers import NewProductSerializer
from decimal import Decimal, InvalidOperation


User = get_user_model()


class Slider_serializer(serializers.ModelSerializer):
    class Meta:
        model = Slider
        fields = ['id', 'images', 'created_at', 'updated_at']


class Stock_serializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ['id', 'images', 'created_at', 'updated_at']


class Brand_serializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ["id", "url", "images", "category", "product", "created_at", "updated_at"]


class WishlistItemSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    product = NewProductSerializer(read_only=True)

    class Meta:
        model = Add_to_wishlist
        fields = ('id', 'user', 'product', 'created_at', 'updated_at')


class WishlistCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Add_to_wishlist
        fields = ('id', 'user', 'product', 'created_at', 'updated_at')

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
        serialized_obj2 = model_to_dict(us)
        serialized_obj['brand'] = [model_to_dict(brand) for brand in pr.brand.all()]
        serialized_obj['color'] = [model_to_dict(color) for color in pr.color.all()]
        data['product'] = serialized_obj
        data['media'] = media_urls
        data['user'] = serialized_obj2
        return data

class CurrencyExchangeSerializer(serializers.Serializer):
    title = serializers.CharField()
    code = serializers.CharField()
    cb_price = serializers.DecimalField(max_digits=10, decimal_places=4)
    nbu_buy_price = serializers.DecimalField(max_digits=10, decimal_places=4)
    nbu_cell_price = serializers.DecimalField(max_digits=10, decimal_places=4)
    date = serializers.DateTimeField()