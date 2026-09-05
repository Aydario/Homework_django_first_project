from django.contrib import admin

from advertisements.models import Advertisement


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'status', 'creator', 'created_at']
    list_filter = ['status', 'creator', 'created_at']
    search_fields = ['title', 'description']
    