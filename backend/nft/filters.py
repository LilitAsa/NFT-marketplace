import django_filters
from .models import NFT

class NFTFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    category = django_filters.CharFilter(field_name='category__name')
    blockchain = django_filters.CharFilter(field_name='blockchain')
    is_listed = django_filters.BooleanFilter(field_name='is_listed')
    owner = django_filters.CharFilter(field_name='owner__username')
    creator = django_filters.CharFilter(field_name='creator__username')
    
    class Meta:
        model = NFT
        fields = {
            'name': ['icontains'],
            'token_standard': ['exact'],
            'status': ['exact'],
        }