from django.shortcuts import render
from rest_framework import generics
from .models import Checkout, CartItem
from .serializers import CheckoutSerializer, CheckoutAllSerializer


class CheckoutList(generics.CreateAPIView):
    queryset = Checkout.objects.all()
    serializer_class = CheckoutSerializer

    def perform_create(self, serializer):
        # Изменяем cart_status на True перед сохранением объекта Checkout
        cart_items = self.request.data.get('cart', [])
        CartItem.objects.filter(id__in=cart_items).update(cart_status=True)

        # Сохраняем объект Checkout
        serializer.save()


class CheckoutDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Checkout.objects.all()
    serializer_class = CheckoutAllSerializer


class CheckoutDetailAll(generics.ListAPIView):
    queryset = Checkout.objects.all()
    serializer_class = CheckoutAllSerializer
