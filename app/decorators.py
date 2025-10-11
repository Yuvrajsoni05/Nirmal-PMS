
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache, cache_control
from functools  import wraps



def custom_login_required(view_func):
    @never_cache
    @cache_control(no_store=True, no_cache=True, must_revalidate=True, max_age=0)
    @login_required(redirect_field_name=None)
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login_page')
        return view_func(request, *args, **kwargs)
    return wrapper