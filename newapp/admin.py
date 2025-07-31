from django.contrib import admin
from .models import DynamicsCourse

@admin.register(DynamicsCourse)
class DynamicsCourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
