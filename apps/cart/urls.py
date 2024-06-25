from rest_framework.routers import DefaultRouter
from .views import  CartAPIView, ALLCartListAPIView, CartCreateAPIView, CartDeleteAPIView, CartUpdateAPIView

from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'delete-cart', CartDeleteAPIView)

urlpatterns = [
    path('', include(router.urls)),
    path('all-carts', ALLCartListAPIView.as_view()),
    path('user-carts/<int:pk>', CartAPIView.as_view()),
    path('add-cart', CartCreateAPIView.as_view()),
    path('update-cart/<int:pk>', CartUpdateAPIView.as_view())
]