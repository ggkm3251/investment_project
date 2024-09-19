from django.contrib import admin

from investment.models import InvestmentAccount, Transaction

# Register your models here.

admin.site.register(InvestmentAccount)
admin.site.register(Transaction)