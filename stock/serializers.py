from rest_framework import serializers
from .models import Stock, StockTransaction


class StockSerializer(serializers.ModelSerializer):
    sku = serializers.IntegerField(
        required=False,
        allow_null=True
    )
    """
    Serializer for Stock model.
    """
    class Meta:
        model = Stock
        fields = '__all__'


class StockTransactionSerializer(serializers.ModelSerializer):
    """
    Serializer for StockTransaction model with nullable fields.
    """
    stock = serializers.PrimaryKeyRelatedField(
        queryset=Stock.objects.all(),
        required=False,
        allow_null=True
    )
    transaction_type = serializers.CharField(
        required=False,
        allow_null=True
    )
    quantity = serializers.IntegerField(
        required=False,
        allow_null=True
    )

    class Meta:
        model = StockTransaction
        fields = '__all__'
