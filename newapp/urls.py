from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns=[
    path('',views.home, name="index"), 
    path('courses/<slug:slug>/', views.course_detail, name='course_detail'),
    path('about/', views.about, name='about'),
    path('become-instructor/', views.instructor, name='become_instructor'),
    path('contact/', views.contact_view, name='contact'),
    path('blogs/', views.blog_view, name='blog_list'),
    path('signup/', views.signup, name='signup'),
    path('user-login/', views.user_login, name='user-login'),
    path('user-logout/', views.user_logout, name='user-logout'),
]