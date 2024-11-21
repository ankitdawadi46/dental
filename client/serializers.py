from rest_framework.serializers import ModelSerializer, Serializer

from client.models import Client


class DashboardSerializer(Serializer):
    pass


class ClientSerializer(ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"
