from django.contrib import admin
from .models import Course, UpcomingBatch, Module, Blog


class ModuleInline(admin.TabularInline):
    model = Module
    extra = 1  # Number of empty modules to show by default
    fields = ('title', 'description')  # this is my code

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

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['title', 'author', 'content']
    actions = ['approve_blogs']

    def approve_blogs(self, request, queryset):
        queryset.update(status='approved')
    approve_blogs.short_description = "Mark selected blogs as approved"