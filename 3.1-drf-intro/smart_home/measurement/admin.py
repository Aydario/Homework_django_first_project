from django.contrib import admin
from .models import Sensor, Measurement

@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description']
    list_display_links = ['id', 'name']
    search_fields = ['name', 'description']

@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    list_display = ['id', 'sensor', 'temperature', 'created_at']
    list_filter = ['sensor', 'created_at']
    search_fields = ['sensor__name']
    date_hierarchy = 'created_at'
