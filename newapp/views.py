
from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, UpcomingBatch
from .forms import RegisterForm,LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def home(request):
    courses = Course.objects.all()
    # courses = DynamicsCourse.objects.all()
    return render(request, 'index.html', {'courses': courses })

 # <-- apna custom form import

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # optional: auto login
            messages.success(request, "Account created successfully!")
            return redirect('login')  # home page ka url name
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})

    
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect('index')  
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')


def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug)
    upcoming_batches = UpcomingBatch.objects.all().order_by('start_date')
    return render(request, 'course_detail.html', {'course': course,'upcoming_batches': upcoming_batches})

