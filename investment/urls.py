from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InvestmentAccountViewSet, TransactionViewSet

# Initialize the default router
router = DefaultRouter()

# Register viewsets with the router
router.register(r'accounts', InvestmentAccountViewSet)
router.register(r'transactions', TransactionViewSet)



urlpatterns = [
    path('', include(router.urls)),
]
