from rest_framework.permissions import BasePermission

from investment.models import AccountPermission, UserProfile


class HasAccountPermission(BasePermission):

    #Custom permission to grant users specific access to investment accounts and transactions based on their permission level in AccountPermission.

    def has_object_permission(self, request, view, obj):
        
        #Determine if the user has permission to perform the given action on the account or transaction.
    

        try:
            # Fetch the user profile associated with the request user
            user_profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            return False
        
        # Fetch the AccountPermission object for the user and the account
        account_permission = AccountPermission.objects.filter(
            user_profile=user_profile, account=obj if hasattr(obj, 'balance') else obj.account
        ).first()

        if not account_permission:
            return False
        
        # Permission logic for different actions:
        # Read (retrieve, list) permissions
        if view.action in ['list', 'retrieve']:
            return account_permission.permission_level in ['view', 'full']
        
        # Create (post transactions) permissions
        if view.action == 'create':
            return account_permission.permission_level in ['post', 'full']
        
        # Update/Delete permissions (only full access)
        if view.action in ['update', 'partial_update', 'destroy']:
            return account_permission.permission_level == 'full'
        
        return False

