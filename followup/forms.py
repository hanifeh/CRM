from django import forms
from . import models


class FollowUpCreateForm(forms.ModelForm):
    """
    form for create one follow up (add creator and organization automatic)
    """
    def __init__(self, *args, **kwargs):
        self.creator = kwargs.pop('creator')
        self.organization = kwargs.pop('organization')
        super().__init__(*args, **kwargs)

    class Meta:
        model = models.FollowUp
        fields = [
            'title',
            'body',
        ]
