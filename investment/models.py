from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username

class InvestmentAccount(models.Model):
    name = models.CharField(max_length=255)
    users = models.ManyToManyField(UserProfile, through='AccountPermission', related_name='investment_accounts')
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return self.name
    
class AccountPermission(models.Model):
    PERMISSION_CHOICES = [
        ('view', 'Can view transactions'),
        ('post', 'Can post transactions'),
        ('full', 'Full access (CRUD)'),
    ]

    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    account = models.ForeignKey(InvestmentAccount, on_delete=models.CASCADE)
    permission_level = models.CharField(max_length=10, choices=PERMISSION_CHOICES)

    class Meta:
        unique_together = ('user_profile', 'account')

    def __str__(self):
        return f'{self.user_profile.user.username} - {self.account.name} - {self.permission_level}'

class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
    ]

    account = models.ForeignKey(InvestmentAccount, on_delete=models.CASCADE, related_name='transactions')
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=[('deposit', 'Deposit'), ('withdrawal', 'Withdrawal')], default='deposit')  # Add default here
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.account.name} - {self.amount} by {self.user_profile.user.username}'
    
    def save(self, *args, **kwargs):
        # Validate permission level
        account_permission = AccountPermission.objects.get(user_profile=self.user_profile, account=self.account)
        
        if account_permission.permission_level not in ['post', 'full']:
            raise PermissionDenied(f"{self.user_profile.user.username} does not have permission to post transactions for this account.")
        
        # Adjust the account balance based on the transaction type
        if self.transaction_type == 'deposit':
            self.account.balance += self.amount
        elif self.transaction_type == 'withdrawal':
            if self.account.balance < self.amount:
                raise ValueError("Insufficient funds for this transaction.")
            self.account.balance -= self.amount

        self.account.save()  # Save the updated balance
        super(Transaction, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Adjust the account balance when a transaction is deleted
        if self.transaction_type == 'deposit':
            self.account.balance -= self.amount
        elif self.transaction_type == 'withdrawal':
            self.account.balance += self.amount
        
        self.account.save()  # Save the updated balance
        super(Transaction, self).delete(*args, **kwargs)
