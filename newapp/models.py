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
    video = models.FileField(upload_to='courses/videos/', blank=True, null=True)
    syllabus_link = models.CharField(max_length=255, blank=True, null=True) 

    def __str__(self):
        return self.title
