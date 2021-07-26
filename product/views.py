from django.views.generic import ListView
from product import models


class ViewListProducts(ListView):
    """
    :return List of Products
    """
    model = models.Product
    template_name = 'list-products.html'

    def get_queryset(self):
        products = models.Product.objects.all()
        return products
