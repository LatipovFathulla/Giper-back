import django_filters
from django.db.models import Q
from django_filters import rest_framework as filters
from .models import NewProductModel, ProductAttributeValue, Category, Brand


class ProductInventoryFilter(django_filters.FilterSet):
    # sku = django_filters.CharFilter(lookup_expr='icontains')
    # upc = django_filters.CharFilter(lookup_expr='icontains')
    # product_type = django_filters.NumberFilter()
    # attributes = django_filters.NumberFilter()
    #
    # class Meta:
    #     model = ProductInventory
    #     fields = ['sku', 'upc', 'product_type', 'attributes']
    brand = filters.ModelMultipleChoiceFilter(
        queryset=Brand.objects.all(),
        field_name='brand__name',
        lookup_expr='exact',
    )
    attribute_values = filters.ModelMultipleChoiceFilter(
        queryset=ProductAttributeValue.objects.all(),
        field_name='attribute_values',
        to_field_name='id',
    )
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    category = django_filters.CharFilter(method='filter_category')

    def filter_category(self, queryset, name, value):
        # Get the category object that matches the provided slug
        try:
            category = Category.objects.get(name=value)
        except Category.DoesNotExist:
            return queryset.none()

        # Get all products that belong to the matching category or its children
        products = queryset.filter(category__in=category.get_descendants(include_self=True))

        return products


    class Meta:
        model = NewProductModel
        fields = ['attribute_values', 'price', 'is_recommend', 'category', 'color']
