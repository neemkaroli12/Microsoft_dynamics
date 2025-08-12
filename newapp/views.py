
from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, UpcomingBatch
from .forms import RegisterForm,LoginForm,InstructorApplicationForm,ContactForm 
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.mail import EmailMessage
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
    success = False

    if request.method == 'POST':
        form = InstructorApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            full_name = form.cleaned_data['full_name']
            country_code = form.cleaned_data['country_code']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            current_city = form.cleaned_data['current_city']
            course_topic = form.cleaned_data['course_topic']
            linkedin_url = form.cleaned_data['linkedin_url']
            about_yourself = form.cleaned_data['about_yourself']
            cv_file = form.cleaned_data.get('cv')

            # Handle CV upload if exists
            if cv_file:
                fs = FileSystemStorage()
                filename = fs.save(cv_file.name, cv_file)
                uploaded_file_url = fs.url(filename)
                # Save or process the URL as needed

            # Save other form data or send email etc.

            success = True
            form = InstructorApplicationForm()  # clear the form after success
    else:
        form = InstructorApplicationForm()

    return render(request, 'instructor.html', {'form': form, 'success': success})

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


