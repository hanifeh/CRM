from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from django_jalali.db import models as jmodels


class Product(models.Model):
    """
    A product sell by company
    """
    name = models.CharField(max_length=50, unique=True, verbose_name=_('product name'))
    slug = models.SlugField(max_length=50, unique=True, editable=False)
    created_date = jmodels.jDateField(auto_now_add=True, verbose_name=_('product created date'))
    price = models.PositiveIntegerField(verbose_name=_('product price'))
    tax_status = models.BooleanField(default=True, verbose_name=_('product tax status'))
    technical_specification = models.TextField(verbose_name=_('product technical specification'))
    catalogue_image = models.ImageField(upload_to='image', blank=True, null=True,
                                        verbose_name=_('product catalogue image'))
    catalogue_pdf = models.FileField(upload_to='pdf', blank=True, null=True, verbose_name=_('product catalogue pdf'))

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        auto add slug
        """
        if not self.id:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)
