from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Sum, F
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

    def get_total_quantity(self):
        return self.quoteitem_set.aggregate(Sum('quantity')).get('quantity__sum', 0)

    def get_total_start_price(self):
        total_start_price = 0
        for item in self.quoteitem_set.all():
            total_start_price += item.quantity * item.product.price
        return int(total_start_price)

    def get_quote_tax(self):
        quote_tax = 0
        for item in self.quoteitem_set.all():
            quote_tax += item.get_total_tax()
        return int(quote_tax)

    def get_quote_discount(self):
        quote_discount = 0
        for item in self.quoteitem_set.all():
            quote_discount -= item.get_total_discount()
        return int(quote_discount)

    def get_total_price(self):
        total_price = 0
        for item in self.quoteitem_set.all():
            total_price += item.get_total_price()
        return int(total_price)


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

    def get_total_start_price(self):
        return self.quantity * self.product.price

    def get_total_price(self):
        total_price = self.get_total_start_price()
        if self.discount:
            total_price -= (self.discount * total_price / 100)
        if self.product.tax_status:
            total_price += (9 * total_price / 100)
        return int(total_price)

    def get_total_discount(self):
        total_discount = 0
        if self.discount:
            total_discount = (self.discount * (self.get_total_start_price()) / 100)
        return int(total_discount)

    def get_total_tax(self):
        total_tax = 0
        if self.product.tax_status:
            total_tax = (9 * (self.get_total_start_price()-self.get_total_discount()) / 100)
        return int(total_tax)
