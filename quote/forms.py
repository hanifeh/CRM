from . import models
from django.forms import modelformset_factory


QuoteItemCreateFormSet = modelformset_factory(models.QuoteItem, fields=('product', 'quantity', 'discount'), extra=1)
