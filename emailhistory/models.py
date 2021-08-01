from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_jalali.db import models as jmodels


class EmailHistory(models.Model):
    """
    EmailHistory is result of send email
    """
    creator = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, verbose_name=_('creator'))
    create_time = jmodels.jDateTimeField(auto_now_add=True, verbose_name=_('create time'))
    email_status = models.BooleanField(default=True, verbose_name=_('email status'))
    email = models.CharField(max_length=50, verbose_name=_('email'))

    class Meta:
        verbose_name = _('email history')
        verbose_name_plural = _('emails history')
