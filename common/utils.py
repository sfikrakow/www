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
