from rest_framework import viewsets, generics, mixins
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
import requests
from rest_framework.decorators import api_view

from .models import Slider, Stock, Brand, Add_to_wishlist
from .serializers import Slider_serializer, Stock_serializer, Brand_serializer, WishlistCreateSerializer, \
    WishlistItemSerializer
from ..products.permission import ModelViewSetsPermission


class Sliderviews(viewsets.ModelViewSet):
    permission_classes = (ModelViewSetsPermission,)
    serializer_class = Slider_serializer
    queryset = Slider.objects.all()
    http_method_names = ("get",)


class Stockviews(viewsets.ModelViewSet):
    permission_classes = (ModelViewSetsPermission,)
    serializer_class = Stock_serializer
    queryset = Stock.objects.all()
    http_method_names = ("get",)


class Brandviews(viewsets.ModelViewSet):
    permission_classes = (ModelViewSetsPermission,)
    serializer_class = Brand_serializer
    queryset = Brand.objects.all()
    http_method_names = ("get",)


# class Add_to_cartviews(APIView):
#     serializer_class = Add_to_cart_serializer
#
#
#
#     def get(self, request, format=None):
#         transformers = Add_to_cart.objects.all()
#         serializer = Brand_serializer(transformers, many=True)
#         return Response(serializer.data)

class WishlistAPIView(APIView):
    def get(self, request, pk):
        wishlist = Add_to_wishlist.objects.filter(user_id=pk)
        serializer = WishlistItemSerializer(wishlist, context={'request': request}, many=True)
        return Response(serializer.data)


class WishlistCreateAPIView(generics.CreateAPIView):
    queryset = Add_to_wishlist.objects.all()
    serializer_class = WishlistCreateSerializer


class WishlistDeleteAPIView(mixins.DestroyModelMixin, GenericViewSet):
    queryset = Add_to_wishlist.objects.all()
    serializer_class = WishlistCreateSerializer

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class WishlistUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Add_to_wishlist.objects.all()
    serializer_class = WishlistCreateSerializer


@api_view(['GET'])
def exchange_rates(request):
    url = 'https://nbu.uz/uz/exchange-rates/json/'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return Response(data)
    else:
        return Response(status=404)