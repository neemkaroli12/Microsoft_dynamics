from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, get_object_or_404, redirect
from .models import DynamicsCourse
def home(request):
    courses = DynamicsCourse.objects.all()
    return render(request, 'index.html', {'courses': courses})




    