from django.test import TestCase
from .models import Organization
from django.contrib.auth import get_user_model
from django.urls import reverse


class OrganizationTestCase(TestCase):
    """
    Organization testcase
    """

    def test_OrganizationList_auth(self):
        """
        Test  Organization list auth
        """
        response = self.client.get(reverse('organizations:list-organizations'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/users/login', response.url)
        response = self.client.get(reverse('organizations:list-organizations'), follow=True)
        self.assertContains(response, 'Login')

    def test_OrganizationList_with_login(self):
        """
        test Organization list with login user
        """
        user = get_user_model().objects.create(username='user1')
        self.client.force_login(user=user)
        response = self.client.get(reverse('organizations:list-organizations'))
        self.assertEqual(response.status_code, 200)

    def test_OrganizationCreate_auth(self):
        """
        test Organization create auth
        """
        response = self.client.get(reverse('organizations:create-organization'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/users/login', response.url)
        response = self.client.get(reverse('organizations:create-organization'), follow=True)
        self.assertContains(response, 'Login')

    def test_OrganizationCreate_with_login(self):
        """
        test Organization create with login user
        """
        user = get_user_model().objects.create(username='user1')
        self.client.force_login(user=user)
        response = self.client.get(reverse('organizations:create-organization'))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('organizations:create-organization'), {'creator': user,
                                                                                   'name': 'test',
                                                                                   'city': 'testestan',
                                                                                   'organization_phone_number': '02133011254',
                                                                                   'organization_email': 'test@testmail.com',
                                                                                   'number_of_employees': '1',
                                                                                   'purchasing_officer_name': 'testname',
                                                                                   'purchasing_officer_phone_number': '09123546789'})
        self.assertEqual(response.status_code, 302)
        response = self.client.post(reverse('organizations:create-organization'), {'creator': user,
                                                                                   'name': 'test',
                                                                                   'city': 'testestan',
                                                                                   'organization_phone_number': '02133011254',
                                                                                   'organization_email': 'test@testmail.com',
                                                                                   'number_of_employees': '1',
                                                                                   'purchasing_officer_name': 'testname',
                                                                                   'purchasing_officer_phone_number': '09123456789'})
        self.assertEqual(response.status_code, 400)
