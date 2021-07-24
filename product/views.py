from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from product import models


class ViewProductsList(LoginRequiredMixin, ListView):
    """
    :return List of Products
    """
    model = models.Product
    template_name = 'products-list.html'

    def get_queryset(self):
        products = models.Product.objects.all()
        return products
