from django import forms 
from django.contrib.auth.models import User
from .models import InstructorApplication, ContactMessage, Blog, Enrollment
from django.contrib.auth.forms import UserCreationForm
import re

class InstructorApplicationForm(forms.ModelForm):
    class Meta:
        model = InstructorApplication
        fields = [
            'full_name',
            'country_code',
            'phone_number',
            'email',
            'current_city',
            'course_topic',
            'linkedin_url',
            'about_yourself',
            'cv',
        ]
        labels = {
            'cv': 'Upload Your CV (PDF, DOC, DOCX)',
        }
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name*', 'required': True}),
            'country_code': forms.Select(attrs={'class': 'form-select', 'required': True}, choices=[('+91 India', '+91 India')]),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number*', 'required': True}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address*', 'required': True}),
            'current_city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Current City*', 'required': True}),
            'course_topic': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Course Topic*', 'required': True}),
            'linkedin_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'LinkedIn Profile URL*', 'required': True}),
            'about_yourself': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Tell us about yourself*', 'required': True}),
            'cv': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': '.pdf,.doc,.docx'}),
        }

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')

        # Allow only 10 digits (India standard)
        if not re.match(r'^\d{10}$', phone_number):
            raise forms.ValidationError("Phone number must be exactly 10 digits without spaces or symbols.")

        return phone_number


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Message', 'rows': 5}),
        }

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content', 'image', 'author']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
        }


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }   
class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['name', 'email', 'phone', 'course', 'fees']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your Name', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Your Email', 'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Phone Number', 'class': 'form-control'}),
            'course': forms.TextInput(attrs={'placeholder': 'Course Name', 'class': 'form-control'}),
            'fees': forms.NumberInput(attrs={'placeholder': 'Fees', 'class': 'form-control'}),
        }        