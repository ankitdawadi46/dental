from rest_framework.serializers import ModelSerializer, Serializer

from client.models import Client, Domain


class DashboardSerializer(Serializer):
    pass


class ClientSerializer(ModelSerializer):
    
    class Meta:
        model = Client
        fields = "__all__"
        

class DomainSerializer(ModelSerializer):
    
    class Meta:
        model = Domain
        fields = "__all__"
