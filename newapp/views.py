
from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, UpcomingBatch, Blog
from .forms import InstructorApplicationForm,ContactForm ,BlogForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required
def home(request):
    courses = Course.objects.all()
    # courses = DynamicsCourse.objects.all()
    return render(request, 'index.html', {'courses': courses })


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

            success = True
            form = InstructorApplicationForm()  
    else:
        form = InstructorApplicationForm()

    return render(request, 'instructor.html', {'form': form, 'success': success})

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()
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


def blog_view(request):
    if request.user.is_staff:
        # Admin ko sab posts dikhaye
        blogs = Blog.objects.all().order_by('-created_at')
    else:
        # Normal user ko sirf approved dikhaye
        blogs = Blog.objects.filter(is_approved=True, status='approved').order_by('-created_at')

    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            if request.user.is_authenticated:
                blog.author = request.user.get_full_name() or request.user.username
            blog.is_approved = False  # pending approval
            blog.status = 'pending'   # set status explicitly
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
