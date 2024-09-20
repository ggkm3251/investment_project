from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import UserProfile, InvestmentAccount, AccountPermission, Transaction

class InvestmentAPITestCase(APITestCase):

    def setUp(self):
        # Create test user and profile
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.user_profile = UserProfile.objects.create(user=self.user)

        # Create investment account
        self.account = InvestmentAccount.objects.create(name='Test Account', balance=1000)

        # Assign permissions
        AccountPermission.objects.create(user_profile=self.user_profile, account=self.account, permission_level='full')

        # Obtain JWT token
        response = self.client.post(reverse('token_obtain_pair'), {
            'username': 'testuser',
            'password': 'testpass'
        })
        self.token = response.data['access']

        # Set the authorization header for subsequent requests
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_create_transaction_with_full_permission(self):
        url = reverse('transaction-list')
        data = {
            'account': self.account.id,
            'user_profile': self.user_profile.id,
            'transaction_type': 'deposit',
            'amount': 200,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_transaction_without_permission(self):
        # Change permission to 'view' only
        AccountPermission.objects.filter(user_profile=self.user_profile, account=self.account).update(permission_level='view')

        url = reverse('transaction-list')
        data = {
            'account': self.account.id,
            'user_profile': self.user_profile.id,
            'transaction_type': 'deposit',
            'amount': 200,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_investment_account_list(self):
        url = reverse('investmentaccount-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.account.name)
