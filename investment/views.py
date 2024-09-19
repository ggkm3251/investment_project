from django.shortcuts import render

from django.db.models import Sum
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import InvestmentAccount, Transaction, UserProfile
from .serializers import InvestmentAccountSerializer, TransactionSerializer
from .permissions import HasAccountPermission
from django_filters.rest_framework import DjangoFilterBackend


# Create your views here.
class InvestmentAccountViewSet(viewsets.ModelViewSet):
    queryset = InvestmentAccount.objects.all()
    serializer_class = InvestmentAccountSerializer
    permission_classes = [IsAuthenticated, HasAccountPermission]

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated, HasAccountPermission]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['account', 'date']
    ordering_fields = ['date']

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def admin_summary(self, request):
        user_profile = UserProfile.objects.get(user=request.user)
        transactions = Transaction.objects.filter(user_profile=user_profile)
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        if start_date and end_date:
            transactions = transactions.filter(date__range=[start_date, end_date])

        total_balance = transactions.aggregate(Sum('amount'))['amount__sum'] or 0

        serialized = TransactionSerializer(transactions, many=True)
        return Response({
            'transactions': serialized.data,
            'total_balance': total_balance
        })