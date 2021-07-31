from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Sum, F, Case, When
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
        """
        :return: total quantity in all quote items
        """
        return self.quoteitem_set.all().aggregate(Sum('quantity')).get('quantity__sum', 0)

    def get_total_start_price(self):
        """
        :return: total price before discount and tax
        """
        return self.quoteitem_set.all().annotate(total_start_price=F('quantity') * F('price')) \
            .aggregate(Sum('total_start_price'))['total_start_price__sum']

    def get_quote_discount(self):
        """
        :return: total discount
        """
        return self.quoteitem_set.all().annotate(
            total_start_price=F('quantity') * F('price')).annotate(
            total_discount=(F('discount') * F('total_start_price') / 100)) \
            .aggregate(Sum('total_discount'))['total_discount__sum']

    def get_quote_tax(self):
        """
        :return: total tax
        """
        return self.quoteitem_set.all().annotate(
            total_start_price=F('quantity') * F('price')).annotate(
            total_price=F('total_start_price') - (F('discount') * F('total_start_price') / 100)).annotate(
            total_tax=Case(
                When(product__tax_status=True, then=(F('total_price') * 9 / 100)),
                When(product__tax_status=False, then=0),
                output_field=models.PositiveIntegerField()
            )
        ).aggregate(Sum('total_tax'))['total_tax__sum']

    def get_total_price(self):
        """
        :return: total price after discount and tax
        """
        return self.quoteitem_set.all().annotate(
            total_start_price=F('quantity') * F('price')).annotate(
            total_price=F('total_start_price') - (F('discount') * F('total_start_price') / 100)).annotate(
            total_price=Case(
                When(product__tax_status=True, then=F('total_price') + (F('total_price') * 9 / 100)),
                When(product__tax_status=False, then=F('total_price')),
                output_field=models.PositiveIntegerField()
            )
        ).aggregate(Sum('total_price'))['total_price__sum']


class QuoteItem(models.Model):
    """
    A single item in the quote
    """
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE, verbose_name=_('quote'))
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name=_('product'))
    price = models.PositiveIntegerField(default=0, verbose_name=_('price'))
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)], verbose_name=_('quantity'))
    discount = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(100)], verbose_name=_('discount'))

    def __str__(self):
        return f'{self.quote} {self.product}'

    def get_total_price(self):
        return self.quantity * self.price
