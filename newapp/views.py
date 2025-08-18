
from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, UpcomingBatch, Blog, Enrollment
from .forms import InstructorApplicationForm,ContactForm ,BlogForm,CustomUserCreationForm,EnrollmentForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import re
def home(request):
    courses = Course.objects.all()
    # courses = DynamicsCourse.objects.all()
    return render(request, 'index.html', {'courses': courses })

from django.http import JsonResponse

@csrf_exempt
def enroll_course(request):
    if request.method == "POST":
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            enrollment = form.save()  # saves to DB

            # Send email to user + admin
            subject = f"Enrollment Confirmation: {enrollment.course}"
            message = f"""
Hi {enrollment.name},

Thank you for enrolling in {enrollment.course}.

Details:
Name: {enrollment.name}
Email: {enrollment.email}
Phone: {enrollment.phone}
Course: {enrollment.course}
Fees: {enrollment.fees}

We will contact you soon.

Best regards,
NIITF Team
"""
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [enrollment.email,'info@niitf.com'],
                fail_silently=False
            )

            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False, "errors": form.errors})
    return JsonResponse({"success": False, "error": "Invalid request method."})




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
            if cv_file:
                fs = FileSystemStorage()
                filename = fs.save(cv_file.name, cv_file)
                uploaded_file_url = fs.url(filename)
            else:
                uploaded_file_url = "No CV uploaded"
            subject = f"New Instructor Application: {full_name}"
            message = f"""
Full Name: {full_name}
Country Code: {country_code}
Phone: {phone_number}
Email: {email}
City: {current_city}
Course Topic: {course_topic}
LinkedIn: {linkedin_url}
About Yourself: {about_yourself}
CV: {uploaded_file_url}
"""
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                ['info@niitf.com'],  
                fail_silently=False
            )

            success = True
            
    else:
        form = InstructorApplicationForm()

    return render(request, 'instructor.html', {'form': form, 'success': success})

def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # Send email
            send_mail(
                subject=f"New message from {name}",
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,  
                recipient_list=['info@niitf.com'],  # <- send to your email
                fail_silently=False,
            )



            return render(request, 'contact.html', {'form': ContactForm(), 'success': True})
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})


def blog_view(request):
    if request.user.is_staff:
       
        blogs = Blog.objects.all().order_by('-created_at')
    else:
        blogs = Blog.objects.filter(is_approved=True, status='approved').order_by('-created_at')

    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            if request.user.is_authenticated:
                blog.author = request.user.get_full_name() or request.user.username
            blog.is_approved = False  
            blog.status = 'pending'   
            blog.save()
            return redirect('blog_list')
    else:
        initial_data = {}
        if request.user.is_authenticated:
            initial_data['author'] = request.user.get_full_name() or request.user.username
        form = BlogForm(initial=initial_data)

    context = {
        'blogs': blogs,
        'form': form,
        'is_admin': request.user.is_staff,
    }
    return render(request, 'blog.html', context)


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully Signed up')
            return redirect('user-login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully logged in')
            return redirect('index')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')
def user_logout(request):
    logout(request)
    return redirect('user-login')