from rest_framework import serializers
from .models import InvestmentAccount, Transaction, AccountPermission, UserProfile

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'account', 'user_profile', 'amount', 'date']

class InvestmentAccountSerializer(serializers.ModelSerializer):
    transactions = TransactionSerializer(many=True, read_only=True)

    class Meta:
        model = InvestmentAccount
        fields = ['id', 'name', 'balance', 'transactions']
