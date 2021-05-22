import django_filters
from django_filters import CharFilter

class filterVcanteen(django_filters.FilterSet):
    search = CharFilter(field_name='item', lookup_expr='icontains')
    
class filterVlounge(django_filters.FilterSet):
    search = CharFilter(field_name='item', lookup_expr='icontains')
