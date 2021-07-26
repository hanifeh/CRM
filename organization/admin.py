from django.contrib import admin
from .models import Organization, OrganizationProduct


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    """
    organization admin setting
    """
    list_display = (
        'name',
        'city',
        'organization_phone_number',
        'organization_email',
        'get_organization_products',
        'purchasing_officer_name',
        'purchasing_officer_phone_number',
    )
    search_fields = (
        'name__icontains',
        'purchasing_officer_name__icontains',
    )
    list_filter = (
        'city',
        'organization_products',
    )


@admin.register(OrganizationProduct)
class OrganizationProductAdmin(admin.ModelAdmin):
    """
    organization product admin setting
    """
    list_display = (
        'name',
        'get_products_suggestion',
    )
    list_filter = (
        'products_suggestion',
    )
    search_fields = (
        'name__icontains',
    )
