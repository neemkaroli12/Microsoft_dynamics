from django.contrib import admin
from .models import Course, UpcomingBatch, Module, Blog


class ModuleInline(admin.TabularInline):
    model = Module
    extra = 1  
    fields = ('title', 'description') 

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'course_duration', 'assignments_duration','course_fees')
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
    
    
# newapp/admin.py
from django.contrib.admin import AdminSite
from django.contrib.auth.views import LoginView
from django.urls import path

class CustomAdminLoginView(LoginView):
    template_name = 'admin/login.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        # Admin ke liye alag cookie set karo
        response.set_cookie(
            key="admin_sessionid",
            value=self.request.session.session_key,
            httponly=True,
            samesite='Lax'
        )
        return response

class MyAdminSite(AdminSite):
    site_header = "My Custom Admin"
    site_title = "Custom Admin"
    index_title = "Welcome to Custom Admin Panel"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('login/', CustomAdminLoginView.as_view(), name='login'),
        ]
        return custom_urls + urls

# Instance
admin_site = MyAdminSite(name='myadmin')
