from .models import Course

def all_courses(request):
    # Only courses with slug & in Microsoft Dynamics category
    return {
        'courses': Course.objects.filter(
            category="Microsoft Dynamics"
        ).exclude(slug__isnull=True).exclude(slug__exact='')
    }
