from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

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
    permission_level = models.CharField(max_length=4, choices=PERMISSION_CHOICES)

    class Meta:
        unique_together = ('user', 'account')

    def __str__(self):
        return f'{self.user.username} - {self.account.name} - {self.permission_level}'

class Transaction(models.Model):
    account = models.ForeignKey(InvestmentAccount, on_delete=models.CASCADE, related_name='transactions')
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.account.name} - {self.amount} by {self.user.username}'
