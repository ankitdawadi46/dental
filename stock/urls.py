from django.urls import include, path
from rest_framework.routers import DefaultRouter

from stock.views import StockTransactionViewSet, StockViewSet

app_name = "stock"

router = DefaultRouter()
router.register(
    r"stock", StockViewSet, basename="stock"
)
router.register(
    r"stock-transaction",
    StockTransactionViewSet,
    basename="stock_transaction",
)

urlpatterns = [
    path("", include(router.urls)),
]
