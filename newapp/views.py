
from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, UpcomingBatch
from .forms import RegisterForm,LoginForm,InstructorApplicationForm,ContactForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

def home(request):
    courses = Course.objects.all()
    # courses = DynamicsCourse.objects.all()
    return render(request, 'index.html', {'courses': courses })



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
    course = get_object_or_404(Course.objects.prefetch_related('modules'), slug=slug)
    upcoming_batches = UpcomingBatch.objects.all().order_by('start_date')
    return render(request, 'course_detail.html', {'course': course,'upcoming_batches': upcoming_batches})
   
def about(request):
    return render(request, "about.html")

def instructor(request):
    if request.method == 'POST':
        form = InstructorApplicationForm(request.POST)
        if form.is_valid():
            application = form.save()

            # Email
            subject = f"New Instructor Application - {application.full_name}"
            message = (
                f"Full Name: {application.full_name}\n"
                f"Country Code: {application.country_code}\n"
                f"Phone Number: {application.phone_number}\n"
                f"Email: {application.email}\n"
                f"Current City: {application.current_city}\n"
                f"Course Topic: {application.course_topic}\n"
                f"LinkedIn URL: {application.linkedin_url}\n"
                f"About Yourself:\n{application.about_yourself}\n"
            )
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                ['info@niitf.com'],
                fail_silently=False
            )

            messages.success(request, "✅ Your application has been submitted successfully!")
            form = InstructorApplicationForm()  # empty form after submit
    else:
        form = InstructorApplicationForm()

    return render(request, 'instructor.html', {'form': form})


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()

            # Send email
            subject = f"New Contact Message from {contact.name}"
            body = f"""
            Name: {contact.name}
            Email: {contact.email}
            Subject: {contact.subject}
            Message:
            {contact.message}
            """
            send_mail(
                subject,
                body,
                settings.DEFAULT_FROM_EMAIL,
                ['info@niitf.com'],  # change to your email
                fail_silently=False
            )

            messages.success(request, "✅ Your message has been sent successfully!")
            form = ContactForm()  # Clear form
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})
