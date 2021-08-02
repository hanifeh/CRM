from django.test import TestCase, Client
from .models import Product
from django.contrib.auth import get_user_model
from django.urls import reverse


class ProductTestCase(TestCase):
    """
    product testcase
    """

    def test_Product(self):
        """
        Test  product
        """
        response = self.client.get(reverse('products:list-products'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Products')
        self.assertNotContains(response, 'Search')
        Product.objects.create(name='test product', price=2000, tax_status=True, technical_specification='test')
        response = self.client.get(reverse('products:list-products'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Catalogue')
        self.assertNotContains(response, 'Image')
