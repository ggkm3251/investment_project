from rest_framework import serializers
from .models import InvestmentAccount, Transaction, AccountPermission, UserProfile

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'account', 'user_profile', 'amount', 'date']


