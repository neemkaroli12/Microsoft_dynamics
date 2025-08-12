from django.contrib import admin
from .models import Course, UpcomingBatch, Module


class ModuleInline(admin.TabularInline):
    model = Module
    extra = 1  
    fields = ('title', 'description') 

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'course_duration', 'assignments_duration')
    inlines = [ModuleInline]  # Defined after ModuleInline


@admin.register(UpcomingBatch)
class UpcomingBatchAdmin(admin.ModelAdmin):
    list_display = ('start_date', 'batch_type', 'title')
    list_filter = ('batch_type', 'start_date')
    search_fields = ('title', 'schedule_details')


