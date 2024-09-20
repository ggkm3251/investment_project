from rest_framework import serializers
from .models import InvestmentAccount, Transaction, AccountPermission, UserProfile
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'account', 'user_profile', 'transaction_type', 'amount', 'date']

        # Custom validation for permission checking
    def validate(self, data):
        # Get the user profile and account from validated data
        user_profile = data['user_profile']
        account = data['account']
        transaction_type = data['transaction_type']
        
        # Check if the user has permission to post transactions to this account
        try:
            account_permission = AccountPermission.objects.get(user_profile=user_profile, account=account)
        except AccountPermission.DoesNotExist:
            raise PermissionDenied("User does not have permission for this account.")

        # Only allow users with 'post' or 'full' permission to create transactions
        if account_permission.permission_level not in ['post', 'full']:
            raise PermissionDenied(f"{user_profile.user.username} does not have permission to post transactions.")
        
        # Check for sufficient funds in case of withdrawal
        if transaction_type == 'withdrawal' and account.balance < data['amount']:
            raise serializers.ValidationError("Insufficient funds for this withdrawal.")

        return data

class InvestmentAccountSerializer(serializers.ModelSerializer):
     # Use the nested TransactionSerializer to show transactions under the account
    transactions = TransactionSerializer(many=True, read_only=True)

    class Meta:
        model = InvestmentAccount
        fields = ['id', 'name', 'balance', 'transactions']

class AccountPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountPermission
        fields = ['user_profile', 'account', 'permission_level']


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
