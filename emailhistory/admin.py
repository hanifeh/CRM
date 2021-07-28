from django.contrib import admin
from .models import EmailHistory


@admin.register(EmailHistory)
class EmailHistoryAdmin(admin.ModelAdmin):
    """
    EmailHistory admin setting
    """
    list_display = (
        'pk',
        'email',
        'creator',
        'email_status',
        'create_time',
    )
    list_display_links = (
        'pk',
        'email',
    )
    search_fields = (
        'email__icontains',
        'creator__icontains',
    )
    list_filter = (
        'creator',
        'create_time',
        'email_status',
    )
