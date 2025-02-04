from rest_framework import serializers
from .models import Stock, StockTransaction


class StockSerializer(serializers.ModelSerializer):
    sku = serializers.CharField(
        required=False,
        allow_null=True
    )
    """
    Serializer for Stock model.
    """
    class Meta:
        model = Stock
        fields = '__all__'


class StockTransactionGetSerializer(serializers.ModelSerializer):
    # stock = StockSerializer(required=False, allow_null=True)

    class Meta:
        model = StockTransaction
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        if isinstance(instance.stock, Stock):
            response['stock'] = StockSerializer(instance.stock).data
        else:
            response['stock'] = None  # or handle the case appropriately
        return response
    

class StockTransactionPostSerializer(serializers.ModelSerializer):
    # stock = StockSerializer(required=False, allow_null=True)

    class Meta:
        model = StockTransaction
        fields = '__all__'

        
    
