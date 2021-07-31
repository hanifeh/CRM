from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from django_jalali.db import models as jmodels
from django.contrib.auth import get_user_model
from organization.models import Organization


class FollowUp(models.Model):
    """
    A Follow up write by one user for one organization
    """
    title = models.CharField(max_length=50, verbose_name=_('follow up title'))
    slug = models.SlugField(max_length=50, unique=True, editable=False)
    created_time = jmodels.jDateTimeField(auto_now_add=True, verbose_name=_('follow up created time'))
    creator = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, verbose_name=_('creator'))
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT, verbose_name=_('organization'))
    body = models.TextField(verbose_name=_('follow up body'))

    class Meta:
        unique_together = [['title', 'organization']]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
        auto add slug
        """
        if not self.id:
            slug = ' '.join((self.organization.name, self.title))
            self.slug = slugify(slug, allow_unicode=True)
        super().save(*args, **kwargs)
