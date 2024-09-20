from django.contrib import admin
from investment.models import AccountPermission, InvestmentAccount, Transaction, UserProfile

@admin.register(InvestmentAccount)
class InvestmentAccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'balance')
    search_fields = ('name',)
    list_filter = ('balance',)
    ordering = ('-balance',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'account', 'user_profile', 'amount', 'date', 'transaction_type')
    search_fields = ('account__name', 'user_profile__user__username')
    list_filter = ('account', 'date', 'transaction_type')
    ordering = ('-date',)

# Optional: Register UserProfile if needed for admin access
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
    search_fields = ('user__username',)

# Register your models with the admin site

@admin.register(AccountPermission)
class AccountPermissionAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'account', 'permission_level')  # Display in admin list view
    search_fields = ('user_profile__user__username', 'account__name')  # Search by user or account name
    list_filter = ('permission_level', 'account')  # Add filters for permission levels and accounts