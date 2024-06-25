import django_filters

from apps.products.models import NewProductModel


class ProductFilter(django_filters.FilterSet):
    name__not = django_filters.CharFilter(field_name='attribute_values', exclude=True)
    name__not__in = django_filters.CharFilter(field_name='attribute_values', method='filter_name_not_in')
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')

    class Meta:
        model = NewProductModel
        fields = ['attribute_values', 'price']

    @staticmethod
    def filter_name_not_in(queryset, _, value):
        return queryset.exclude(attribute_values__in=value.split(','))
