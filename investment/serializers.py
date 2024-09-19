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

class AccountPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountPermission
        fields = ['user_profile', 'account', 'permission_level']

from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserProfile

class UserCreateSerializer(serializers.ModelSerializer):
    # You might add additional fields specific to UserProfile here if needed
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        # Create the user
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email')
        )
        
        # Create the UserProfile
        UserProfile.objects.create(user=user)
        
        return user
