from django import forms
from . import models


class OrganizationCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.creator = kwargs.pop('creator')
        super().__init__(*args, **kwargs)

    class Meta:
        model = models.Organization
        fields = [
            'name',
            'city',
            'organization_phone_number',
            'organization_email',
            'number_of_employees',
            'organization_products',
            'purchasing_officer_name',
            'purchasing_officer_phone_number',
        ]


class OrganizationEditForm(forms.ModelForm):
    class Meta:
        model = models.Organization
        fields = [
            'name',
            'city',
            'organization_phone_number',
            'organization_email',
            'number_of_employees',
            'organization_products',
            'purchasing_officer_name',
            'purchasing_officer_phone_number',
        ]
