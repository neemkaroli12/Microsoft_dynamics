from django.db import models

class DynamicsCourse(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='dynamics_courses/')
    created_at = models.DateTimeField(auto_now_add=True)  # <-- Added

    def __str__(self):
        return self.title

