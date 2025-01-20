from django.core.exceptions import ValidationError
from django.db.models import F
from django.utils.timezone import now
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from client.utils import atomic_transaction, with_tenant_context
from dental_app.utils.response import BaseResponse
from stock.models import Stock, StockTransaction
from stock.serializers import StockSerializer, StockTransactionSerializer


# Create your views here.
class StockViewSet(viewsets.ModelViewSet):
    """
    API for managing stock.
    """

    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = [AllowAny]

    def update_stock_quantity(self, stock, transaction_type, quantity):
        """
        Updates stock quantity based on transaction type.
        """
        # Fetch the current value of stock.quantity_available
        stock.refresh_from_db()  # Ensures the stock object has the latest data from the database

        current_quantity = stock.quantity_available  # Get the actual quantity

        if transaction_type == "IN":
            stock.quantity_available = F("quantity_available") + quantity
        elif transaction_type == "OUT":
            # Check if sufficient stock is available
            if current_quantity < quantity:
                raise ValidationError(f"Insufficient stock for {stock.product_name}.")
            stock.quantity_available = F("quantity_available") - quantity

        # Update last restocked timestamp for IN transactions
        stock.last_restocked_at = (
            now() if transaction_type == "IN" else stock.last_restocked_at
        )

        # Save the stock object
        stock.save()

    def reorder_stock(self, stock):
        """
        Reorders stock if it falls below the minimum stock level.
        """
        if stock.quantity_available < stock.minimum_stock_level:
            # TODO send email for reorder
            pass
            # reorder_quantity = stock.reorder_quantity
            # stock.quantity_available = F("quantity_available") + reorder_quantity
            # stock.save()

    # @with_tenant_context
    @atomic_transaction
    def partial_update(self, request, *args, **kwargs):
        """
        Updates stock quantity or triggers reorder if necessary.
        """
        stock = self.get_object()
        transaction_type = request.data.get("transaction_type")
        quantity = int(request.data.get("quantity", 0))

        if not transaction_type or transaction_type not in ["IN", "OUT"]:
            return BaseResponse(
                data={"detail": "Invalid or missing transaction type."},
                status=400,
            )

        try:
            # Update stock quantity
            self.update_stock_quantity(stock, transaction_type, quantity)

            # Reorder stock if necessary
            self.reorder_stock(stock)

            stock.refresh_from_db()  # Refresh from DB to get updated quantity
            serializer = self.get_serializer(stock)
            return BaseResponse(
                data=serializer.data,
                status=200,
            )

        except ValidationError as e:
            return BaseResponse(data={"detail": str(e)}, status=400)


class StockTransactionViewSet(viewsets.ModelViewSet):
    """
    API for managing stock transactions.
    """

    queryset = StockTransaction.objects.all()
    serializer_class = StockTransactionSerializer
    permission_classes = [AllowAny]

    # @with_tenant_context
    @atomic_transaction
    def create(self, request, *args, **kwargs):
        """
        Creates a stock transaction and updates stock accordingly.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Extract data
        stock_data = serializer.validated_data.get("stock")
        transaction_type = serializer.validated_data.get("transaction_type")
        quantity = serializer.validated_data.get("quantity")

        try:
            # Check if stock exists
            stock = None
            if stock_data:
                stock = Stock.objects.filter(id=stock_data.id).first()
            if not stock:
                # Create a new stock entry
                stock_creation_data = {
                    "product_name": request.data.get("product_name"),
                    "sku": request.data.get("sku"),
                    "description": request.data.get("description", ""),
                    "quantity_available": quantity if transaction_type == "IN" else 0,
                    "minimum_stock_level": request.data.get("minimum_stock_level", 0),
                    "reorder_quantity": request.data.get("reorder_quantity", 0),
                    "cost_price": request.data.get("cost_price", 0.0),
                    "selling_price": request.data.get("selling_price", 0.0),
                    "warehouse_location": request.data.get("warehouse_location", ""),
                }
                stock_serializer = StockSerializer(data=stock_creation_data)
                stock_serializer.is_valid(raise_exception=True)
                stock = stock_serializer.save()
            else:
                # Update stock quantity
                stock_viewset = StockViewSet()
                stock_viewset.update_stock_quantity(stock, transaction_type, quantity)

            # Save the transaction
            serializer.validated_data["stock"] = stock
            self.perform_create(serializer)
            return BaseResponse(data=serializer.data, status=201)

        except ValidationError as e:
            return BaseResponse(data={"detail": str(e)}, status=400)

    def perform_create(self, serializer):
        """
        Override to add timestamps or additional logic if needed.
        """
        serializer.save(transaction_date=now())

    # @with_tenant_context
    @atomic_transaction
    def update(self, request, *args, **kwargs):
        """
        Updates a stock transaction and adjusts stock accordingly.
        """
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        old_quantity = instance.quantity
        old_transaction_type = instance.transaction_type

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        # Extract data
        stock_data = serializer.validated_data.get("stock")
        transaction_type = serializer.validated_data.get("transaction_type")
        quantity = serializer.validated_data.get("quantity")

        try:
            # Get or create stock
            stock = None
            if stock_data:
                stock = Stock.objects.filter(id=stock_data.id).first()
            if not stock:
                raise ValidationError("Stock does not exist.")

            # Reverse old stock adjustment
            stock_viewset = StockViewSet()
            stock_viewset.update_stock_quantity(
                stock, "OUT" if old_transaction_type == "IN" else "IN", old_quantity
            )

            # Apply new stock adjustment
            stock_viewset.update_stock_quantity(stock, transaction_type, quantity)

            # Save the transaction
            serializer.validated_data["stock"] = stock
            self.perform_update(serializer)
            return BaseResponse(data=serializer.data, status=200)

        except ValidationError as e:
            return BaseResponse(data={"detail": str(e)}, status=400)

    # @with_tenant_context
    @atomic_transaction
    def destroy(self, request, *args, **kwargs):
        """
        Deletes a stock transaction and reverts stock accordingly.
        """
        instance = self.get_object()
        stock = instance.stock
        transaction_type = instance.transaction_type
        quantity = instance.quantity

        try:
            # Reverse stock adjustment
            stock_viewset = StockViewSet()
            stock_viewset.update_stock_quantity(
                stock, "OUT" if transaction_type == "IN" else "IN", quantity
            )

            # Delete the transaction
            self.perform_destroy(instance)
            return BaseResponse(data=None, status=204)

        except ValidationError as e:
            return BaseResponse(data={"detail": str(e)}, status=400)

    def perform_update(self, serializer):
        """
        Add timestamps or additional logic during update.
        """
        serializer.save()

    def perform_destroy(self, instance):
        """
        Override default destroy behavior if needed.
        """
        instance.delete()
