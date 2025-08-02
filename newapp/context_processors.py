from .models import Course

def courses_context(request):
    courses = Course.objects.all()
    return {'courses': courses}
