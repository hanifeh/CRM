from django.contrib import admin
from .models import Quote, QuoteItem


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    """
    Quote admin setting
    """
    list_display = (
        'pk',
        'organization',
        'creator',
        'create_time',
    )
    list_display_links = (
        'pk',
        'organization',
    )
    search_fields = (
        'organization__icontains',
    )
    list_filter = (
        'creator',
        'create_time',
    )


@admin.register(QuoteItem)
class QuoteItemAdmin(admin.ModelAdmin):
    """
    Quote Item admin setting
    """
    list_display = (
        'pk',
        'quote',
        'product',
        'quantity',
        'discount',
    )
    list_display_links = (
        'pk',
        'quote',
    )
    list_filter = (
        'product',
    )
    search_fields = (
        'quote__icontains',
        'product__icontains',
    )
    list_editable = (
        'quantity',
        'discount',
    )
