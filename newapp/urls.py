from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns=[
    path('',views.home, name="index"), 
    path('register/', views.register_view, name="register"),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('courses/<slug:slug>/', views.course_detail, name='course_detail'),
    path('about/', views.about, name='about'),
    path('become-instructor/', views.instructor, name='become_instructor'),
    path('contact/', views.contact_view, name='contact'),
    
]