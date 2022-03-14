from rest_framework.routers import DefaultRouter
from django.urls import path, include
from store.api.v1.viewsets import ProductViewSet, CreateTransactionViewSet, GetTransactionViewSet

router = DefaultRouter()
router.register('product', ProductViewSet, basename="product")
router.register('create_transaction', CreateTransactionViewSet, basename="create_transaction")
router.register('show_transaction', GetTransactionViewSet, basename="show_transaction")

urlpatterns = [
    path("", include(router.urls)),
]