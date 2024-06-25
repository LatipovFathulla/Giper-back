from apps.outside import models
from .models import SiteSettings
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class SliderSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Slider
        fields = ('id', 'url', 'images', 'created_at', 'updated_at')


class StockSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Stock
        fields = ('id', 'url', 'images', 'created_at', 'updated_at')


class BrandSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Brand
        fields = ('id', 'url', 'images', 'category', 'product', 'created_at', 'updated_at')


class SiteSettingsSerializers(serializers.ModelSerializer):
    class Meta:
        model = SiteSettings
        exclude = ('phonenumbers', 'site_type')


class PhoneSiteSettingsSerializers(serializers.ModelSerializer):
    class Meta:
        model = SiteSettings
        fields = ('id', 'phonenumbers', 'site_type')
