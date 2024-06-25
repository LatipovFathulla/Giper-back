from rest_framework import viewsets
from django.contrib.auth import get_user_model
from rest_framework.filters import SearchFilter

from . import serializers as serial
from .models import SiteSettings
from rest_framework.permissions import AllowAny
from apps.outside import models
from .serializers import SiteSettingsSerializers, PhoneSiteSettingsSerializers

User = get_user_model()


class SliderViewSet(viewsets.ModelViewSet):
    queryset = models.Slider.objects.all()
    serializer_class = serial.SliderSerializers
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter]
    search_fields = ['id', 'slug']


class StockViewSet(viewsets.ModelViewSet):
    queryset = models.Stock.objects.all()
    serializer_class = serial.StockSerializers
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter]
    search_fields = ['id', 'slug']


class BrandViewSet(viewsets.ModelViewSet):
    queryset = models.Brand.objects.all()
    serializer_class = serial.BrandSerializers
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter]
    search_fields = ['id', 'slug']


class SiteSettingsViewSet(viewsets.ModelViewSet):
    queryset = SiteSettings.objects.all()
    serializer_class = SiteSettingsSerializers
    permission_classes = [AllowAny]


class PhoneSiteSettingsViewSet(viewsets.ModelViewSet):
    queryset = SiteSettings.objects.all()
    serializer_class = PhoneSiteSettingsSerializers
    permission_classes = [AllowAny]
