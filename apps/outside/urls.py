from django.urls import path, include
from .views import Sliderviews, Stockviews, Brandviews, WishlistCreateAPIView, WishlistUpdateAPIView, \
    WishlistDeleteAPIView, WishlistAPIView, exchange_rates
from rest_framework.routers import DefaultRouter

from ..dashboard_api.views import SiteSettingsViewSet, PhoneSiteSettingsViewSet

router = DefaultRouter()

router.register(r"slider", Sliderviews)
router.register(r"stock", Stockviews)
router.register(r"brand", Brandviews)
router.register(r"delete-wishlist", WishlistDeleteAPIView)
router.register(r'site-settings', SiteSettingsViewSet, basename='site-settings')
router.register(r'phone-site-settings', PhoneSiteSettingsViewSet, basename='site-settings')

urlpatterns = [
    path("", include(router.urls)),
    path('user-wishlist/<int:pk>', WishlistAPIView.as_view()),
    path('add-wishlist', WishlistCreateAPIView.as_view()),
    path('update-wishlist/<int:pk>', WishlistUpdateAPIView.as_view()),
    path('exchange-rates/', exchange_rates, name='exchange-rates'),
    # path("Add_to_cart/", Add_to_cartviews.as_view(), name="Add_to_cartviews"),
    #     WishlistCreateAPIView
    # WishlistDeleteAPIView
    # WishlistUpdateAPIView

]
