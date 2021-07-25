from django.core.validators import RegexValidator
from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from django_jalali.db import models as jmodels
from django.contrib.auth import get_user_model

# regex validator
organization_phone_regex = RegexValidator(regex='^0[1-9]{2}[0-9]{8}$', message='organization phone number invalid')
phone_regex = RegexValidator(regex='^09[0-9]{9}$', message='phone number invalid')
number_regex = RegexValidator(regex='^[1-9]{1}[0-9]*$', message='input invalid')


class Organization(models.Model):
    """
    organization is customer
    """
    creator = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, verbose_name=_('creator'))
    create_time = jmodels.jDateTimeField(auto_now_add=True, verbose_name=_('create time'))
    name = models.CharField(max_length=50, verbose_name=_('organization name'))
    slug = models.SlugField(max_length=50, unique=True, editable=False, blank=False, null=False)
    city = models.CharField(max_length=20, verbose_name=_('organization city'))
    organization_phone_number = models.CharField(validators=[organization_phone_regex], max_length=11,
                                                 verbose_name=_('organization phone number'))
    organization_email = models.EmailField(verbose_name=_('organization email address'))
    number_of_employees = models.CharField(validators=[number_regex], max_length=6,
                                           verbose_name=_('number of employees'))
    organization_products = models.ManyToManyField('organization.OrganizationProduct', blank=True)
    purchasing_officer_name = models.CharField(max_length=50, verbose_name=_('purchasing officer name'))
    purchasing_officer_phone_number = models.CharField(validators=[phone_regex], max_length=11,
                                                       verbose_name=_('purchasing officer phone number'))

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        """
        auto add slug
        """
        if not self.id:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_organization_products(self):
        """
        give a list of product name (str)
        """
        return [product.name for product in self.organization_products.all()]

    # change get_organization_products to organization products in admin
    get_organization_products.short_description = 'organization products'

    def get_suggestion_products(self):
        """
        give a list of suggestion products
        """
        products = set()
        for product in self.organization_products.all():
            products |= set(product.get_products_suggestion())
        return list(products)


class OrganizationProduct(models.Model):
    """
    product create by customer
    """
    name = models.CharField(max_length=50, verbose_name=_('organization product name'))
    slug = models.SlugField(max_length=50, unique=True, editable=False, blank=False, null=False)
    created_date = jmodels.jDateField(auto_now_add=True, verbose_name=_('organization product created date'))
    products_suggestion = models.ManyToManyField('product.Product')

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        """
        auto add slug
        """
        if not self.id:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_products_suggestion(self):
        return [product.name for product in self.products_suggestion.all()]

    # change get_products_suggestion to products suggestion in admin
    get_products_suggestion.short_description = 'products suggestion'
