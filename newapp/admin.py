from django.contrib import admin
from .models import DynamicsCourse,Course

@admin.register(DynamicsCourse)
class DynamicsCourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'course_duration', 'assignments_duration')
