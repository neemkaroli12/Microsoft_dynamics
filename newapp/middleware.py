from django.conf import settings

class AdminSessionMiddleware:
    """
    Admin URLs ke liye alag session key handle kare.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Agar admin URL request hai to alag cookie name set karo
        if request.path.startswith('/admin/'):
            request.session_cookie_name = 'admin_sessionid'
        else:
            request.session_cookie_name = settings.SESSION_COOKIE_NAME

        response = self.get_response(request)
        return response
