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