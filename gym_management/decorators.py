from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect

def wymaga_roli(*role_names):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            if request.user.rola in role_names or request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            raise PermissionDenied
        return _wrapped_view
    return decorator