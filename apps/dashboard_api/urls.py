from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter()


router.register(r'sliders', views.SliderViewSet, basename='slider')
router.register(r'stocks', views.StockViewSet, basename='stock')
router.register(r'brands', views.BrandViewSet, basename='brand')

urlpatterns = [
    path('', include(router.urls)),
]

