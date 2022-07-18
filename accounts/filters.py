import django_filters;
from django_filters import DateFilter, CharFilter;
from .models import *;

class OrderFilter(django_filters.FilterSet):
    # Put the name as the same one in the attribute (gte = greather tahn or equal to)
    start_date = DateFilter(field_name="date_created", lookup_expr="gte");
    end_date = DateFilter(field_name="date_created", lookup_expr="lte");
    # icontains = ignore case
    note = CharFilter(field_name="note", lookup_expr='icontains');

    class Meta():
        model = Order;
        fields = '__all__';
        exclude = ['customer', 'date_created'];