import functools

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


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
