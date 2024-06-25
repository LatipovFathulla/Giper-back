from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from .models import  CartItem
from rest_framework import generics, mixins
from rest_framework.response import Response
from .serializers import  CartItemSerializer, CartCreateSerializer



# class CartItemViewSet(viewsets.ModelViewSet):
#     queryset = CartItem.objects.all()
#     serializer_class = CartItemSerializer

class ALLCartListAPIView(generics.ListAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer


class CartAPIView(APIView):
    def get(self, request, pk):
        cart = CartItem.objects.filter(user_id=pk)
        serializer = CartItemSerializer(cart, context={'request': request}, many=True)
        return Response(serializer.data)


class CartCreateAPIView(generics.CreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartCreateSerializer


class CartDeleteAPIView(mixins.DestroyModelMixin, GenericViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartCreateSerializer

    def perform_destroy(self, instance):
        instance.cart_status = True
        instance.save()


class CartUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartCreateSerializer
