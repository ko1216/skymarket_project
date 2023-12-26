import django_filters
from ads.models import Ad


class AdFilter(django_filters.rest_framework.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    author__email = django_filters.CharFilter(field_name='author__email', lookup_expr='icontains')
    price__gte = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price__lte = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    description = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Ad
        fields = ['title', 'author__email', 'price__gte', 'price__lte', 'description']
