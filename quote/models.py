from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_jalali.db import models as jmodels
from django.contrib.auth import get_user_model
from organization.models import Organization
from product.models import Product


class Quote(models.Model):
    """
    quote create by one user for one organization
    """
    creator = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, verbose_name=_('creator'))
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT, verbose_name=_('organization'))
    create_time = jmodels.jDateTimeField(auto_now_add=True, verbose_name=_('create time'))

    def __str__(self):
        return f'{self.organization}'


class QuoteItem(models.Model):
    """
    A single item in the quote
    """
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE, verbose_name=_('quote'))
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name=_('product'))
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)], verbose_name=_('quantity'))
    discount = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(100)], verbose_name=_('discount'))

    def __str__(self):
        return f'{self.quote} {self.product}'
