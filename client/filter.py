import django_filters
from .models import Client

class ClientFilter(django_filters.FilterSet):
    class Meta:
        model = Client
        fields = {
            'name': ['exact'],       # Exact match
            'contact_number': ['exact'],     # Exact match
            'contact_person': ['exact'],
            'email': ['exact'],
            'paid_until': ['gte', 'lte'],
            'primary_domain_name': ['exact']# Range filter (e.g., greater than, less than)
        }