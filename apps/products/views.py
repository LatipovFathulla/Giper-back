from decimal import Decimal
from django.db.models import Q
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from .filter import ProductFilter
from .filters import ProductInventoryFilter
from django.db.models import Min, Max
from .serializers import (
    CategorySerializer,
    RatingSerializer, NewProductSerializer
)
from apps.products.models import Category, Rating, NewProductModel, Brand, ProductAttributeValue, PrColorModel
from rest_framework.response import Response
from rest_framework.views import APIView



class CategoryList(APIView):
    """
    Return list of all categories
    """

    def get(self, request):
        queryset = Category.objects.all()
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)


class ProductByCategory(APIView):
    """
    Return product by category
    """

    def get(self, request, slug=None):
        queryset = NewProductModel.objects.filter(Q(category__slug=slug) | Q(category__parent__slug=slug))
        serializer = NewProductSerializer(queryset, many=True)
        return Response(serializer.data)


class ProductDetailBySlug(APIView):
    """
    Return Sub Product by Slug
    """

    def get(self, request, pk=None):
        product = NewProductModel.objects.get(pk=pk)
        serializer = NewProductSerializer(product, context={'request': request})
        return Response(serializer.data)


class AllProductsView(mixins.ListModelMixin, GenericViewSet):
    """
    Return products
    """
    queryset = NewProductModel.objects.order_by('-pk')
    serializer_class = NewProductSerializer
    filter_backends = [DjangoFilterBackend]
    filter_class = ProductFilter


class USAAllProductsView(mixins.ListModelMixin, GenericViewSet):
    queryset = NewProductModel.objects.order_by('-pk')
    serializer_class = NewProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['USA_product']


class RatingCreate(generics.CreateAPIView):
    """
    Create Rating
    """
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = (IsAuthenticated,)


class ProductFilterView(generics.ListCreateAPIView):
    queryset = NewProductModel.objects.all()
    serializer_class = NewProductSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = ProductInventoryFilter
    search_fields = ('category__slug', 'category__parent__slug')
    ordering_fields = ('price',)
    ordering = ('price',)



from django.db.models import Q

class CategoryBrandListView(APIView):
    paginate_by = None

    def get(self, request, category_id):
        category = Category.objects.get(id=category_id)
        descendants = category.get_descendants(include_self=True)
        products = NewProductModel.objects.filter(Q(category__in=descendants) | Q(category__parent__in=descendants))

        attribute_values = products.exclude(
            attribute_values__product_attribute_id__isnull=True,
            attribute_values__product_attribute__name__isnull=True,
            attribute_values__attribute_value__isnull=True,
        ).values(
            'attribute_values__product_attribute_id',
            'attribute_values__product_attribute__name',
            'attribute_values__attribute_value',
            'attribute_values__id',
            'id'
        )
        brands = products.values('brand__id', 'brand__name',).exclude(brand__isnull=True).distinct()
        color = products.values('color__id', 'color__color').exclude(color__isnull=True).distinct()

        prices = products.aggregate(min_price=Min('price'), max_price=Max('price'))

        return Response({"brands": brands, "attribute_values": attribute_values, "color": color, "min_price": prices['min_price'], "max_price": prices['max_price']})

