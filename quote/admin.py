from django.contrib import admin
from .models import Quote, QuoteItem


class QuoteItemInLine(admin.TabularInline):
    """
    Quote Item In Line setting
    """
    model = QuoteItem
    fields = (
        'product',
        'quantity',
        'price',
        'discount',
    )


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    """
    Quote admin setting
    """
    inlines = [QuoteItemInLine]
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
