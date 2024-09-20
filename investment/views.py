from django.shortcuts import render

from django.db.models import Sum
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import InvestmentAccount, Transaction, UserProfile
from .serializers import InvestmentAccountSerializer, TransactionSerializer, UserCreateSerializer
from .permissions import HasAccountPermission
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import status

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.utils import swagger_auto_schema



# Create your views here.
class InvestmentAccountViewSet(viewsets.ModelViewSet):
    queryset = InvestmentAccount.objects.all()
    serializer_class = InvestmentAccountSerializer
    permission_classes = [IsAuthenticated, HasAccountPermission]

    @swagger_auto_schema(
        operation_description="Retrieve all investment accounts for the authenticated user",
        security=[{"Bearer": []}]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated, HasAccountPermission]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['account', 'date']
    ordering_fields = ['date']

   
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def admin_summary(self, request):
        user_profile =  get_object_or_404(UserProfile, user=request.user)
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
    

class UserCreateView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'user': UserCreateSerializer(user).data,
                'message': 'User and UserProfile created successfully.'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)