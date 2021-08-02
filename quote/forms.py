from . import models
from django import forms
from django.forms import modelformset_factory


class QuoteItemCreateForm(forms.ModelForm):
    """
    form for create one quote item
    """

    class Meta:
        model = models.QuoteItem
        fields = [
            'product',
            'price',
            'quantity',
            'discount',
        ]


QuoteItemCreateFormSet = modelformset_factory(models.QuoteItem, fields=('product', 'price', 'quantity', 'discount'), extra=1)
