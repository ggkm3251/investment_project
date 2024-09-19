from rest_framework.permissions import BasePermission

from investment.models import AccountPermission, UserProfile

from rest_framework.permissions import BasePermission
from investment.models import AccountPermission, UserProfile

class HasAccountPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            return False
        
        account_permission = AccountPermission.objects.filter(
            user_profile=user_profile, account=obj
        ).first()

        if account_permission:
            if view.action in ['list', 'retrieve']:
                return account_permission.permission_level in ['view', 'full']
            if view.action == 'create':
                return account_permission.permission_level in ['post', 'full']
            if view.action in ['update', 'partial_update', 'destroy']:
                return account_permission.permission_level == 'full'
        return False

