from django.db import models


class Course(models.Model):
    CATEGORY_CHOICES = [
        ('Microsoft Dynamics', 'Microsoft Dynamics'),
        ('Odoo', 'Odoo'),
    ]

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)  # <-- New field
    short_description = models.TextField()
    full_description = models.TextField()
    rating = models.FloatField(default=0.0)
    review_count = models.IntegerField(default=0)
    total_learners = models.IntegerField(default=0)
    course_duration = models.CharField(max_length=50, blank=True)
    assignments_duration = models.CharField(max_length=50, blank=True)
    job_oriented_training = models.BooleanField(default=False)
    support_available = models.BooleanField(default=False)
    image = models.ImageField(upload_to='courses/', blank=True, null=True)
    video = models.FileField(upload_to='courses/videos/', blank=True, null=True)
    syllabus_link = models.CharField(max_length=255, blank=True, null=True) 

    def __str__(self):
        return self.title


class UpcomingBatch(models.Model):
    BATCH_TYPE_CHOICES = [
        ('WEEKDAY', 'Weekday'),
        ('WEEKEND', 'Weekend'),
        ('FAST_TRACK', 'Fast Track'),
    ]

    start_date = models.DateField()
    batch_type = models.CharField(max_length=20, choices=BATCH_TYPE_CHOICES)
    title = models.CharField(max_length=255, help_text="Example: Weekdays Regular (Class 1Hr - 1:30Hrs) / Per Session.")
    schedule_details = models.TextField(help_text="Example: (Monday - Friday) Time: 08:00 AM (IST)")
    course_fees = models.IntegerField(blank=True, null=True, help_text="Optional: Link to course fees page")

    def __str__(self):
        return f"{self.start_date} - {self.title}"

class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def _str_(self):
        return f"{self.course.title} - {self.title}"
    
    


class InstructorApplication(models.Model):
    full_name = models.CharField(max_length=150)
    country_code = models.CharField(max_length=20, default='+91 India')
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    current_city = models.CharField(max_length=100)
    course_topic = models.CharField(max_length=150)
    linkedin_url = models.URLField()
    about_yourself = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.course_topic}"
    

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=150)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"

