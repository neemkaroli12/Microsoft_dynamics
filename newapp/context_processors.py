from .models import Course

def all_courses(request):
    return {
        'courses': Course.objects.all()
    }