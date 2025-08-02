from .models import Course

def all_courses(request):
    return {
        'courses': Course.objects.filter(
            category="Microsoft Dynamics"
        ).exclude(slug__isnull=True).exclude(slug__exact='')
    }

    

