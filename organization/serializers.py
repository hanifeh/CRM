from rest_framework import serializers
from . import models


class OrganizationSerializer(serializers.ModelSerializer):
    """
    Serializer class form Organization
    """

    class Meta:
        model = models.Organization
        fields = (
            'name',
            'city',
            'organization_phone_number',
            'organization_email',
            'number_of_employees',
            'organization_products',
            'purchasing_officer_name',
            'purchasing_officer_phone_number',
        )
