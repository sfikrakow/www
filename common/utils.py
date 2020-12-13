import functools

from django.conf import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.utils.http import is_safe_url


def paginate(query, request, items_per_page):
    paginator = Paginator(query, items_per_page)
    page = request.GET.get('page')
    try:
        return paginator.page(page)
    except PageNotAnInteger:
        return paginator.page(1)
    except EmptyPage:
        return paginator.page(paginator.num_pages)


class RenderWithContext:
    def __init__(self, func, args, kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def render(self, context):
        return self.func(*self.args, **self.kwargs, context=context)


def with_context(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return RenderWithContext(func, args, kwargs)

    return wrapper


def get_next_url_post(request, redirect_field_name):
    next_url = request.POST.get(redirect_field_name)
    if next_url:
        kwargs = {
            'url': next_url,
            'require_https': getattr(settings,
                                     'OIDC_REDIRECT_REQUIRE_HTTPS', request.is_secure())
        }

        hosts = list(getattr(settings, 'OIDC_REDIRECT_ALLOWED_HOSTS', []))
        hosts.append(request.get_host())
        kwargs['allowed_hosts'] = hosts

        is_safe = is_safe_url(**kwargs)
        if is_safe:
            return next_url
    return None


def oidc_op_logout(request):
    oidc_op_logout_endpoint = settings.OIDC_OP_LOGOUT_ENDPOINT
    redirect_field_name = getattr(settings, 'OIDC_REDIRECT_FIELD_NAME', 'next')
    redirect_url = get_next_url_post(request, redirect_field_name)
    if redirect_url is None:
        redirect_url = getattr(settings, 'LOGOUT_REDIRECT_URL', '/')
    return '{}?redirect_uri={}'.format(oidc_op_logout_endpoint, request.build_absolute_uri(redirect_url))
