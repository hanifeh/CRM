from django.contrib import admin
from .models import FollowUp


@admin.register(FollowUp)
class FollowUpAdmin(admin.ModelAdmin):
    """
        Follow up admin setting
    """
    list_display = (
        'title',
        'creator',
        'organization',
        'created_time',
    )
    search_fields = (
        'title__icontains',
        'organization__icontains',
    )
    list_filter = (
        'creator',
        'created_time',
    )
