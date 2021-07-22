from django.contrib import admin
from .models import Product


# enable tax
@admin.action(description='tax on')
def tax_status_on(modeladmin, request, queryset):
    queryset.update(tax_status=True)


# disable tax
@admin.action(description='tax off')
def tax_status_off(modeladmin, request, queryset):
    queryset.update(tax_status=False)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
        product admin setting
    """
    list_display = (
        'name',
        'price',
        'technical_specification',
        'tax_status',
        'catalogue_image',
        'catalogue_pdf',
    )
    list_editable = (
        'price',
        'tax_status',
    )
    search_fields = (
        'name__icontains',
        'technical_specification__icontains',
    )
    list_filter = (
        'tax_status',
        'created_date',
    )
    actions = [
        tax_status_on,
        tax_status_off,
    ]
