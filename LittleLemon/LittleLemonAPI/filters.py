import django_filters
from .models import Order

class OrderFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(method='filter_status')

    def filter_status(self, queryset, name, value):
        status_map = {
            "pending": False,  
            "delivered": True 
        }
        if value in status_map:
            return queryset.filter(status=status_map[value])
        return queryset.none()

    class Meta:
        model = Order
        fields = ['status']
