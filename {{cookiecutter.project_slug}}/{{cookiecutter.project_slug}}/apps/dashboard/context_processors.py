from django.http import HttpRequest

from .navigation.sidebar import get_sidebar_items


def sidebar_context(request: HttpRequest):
    """
    Add sidebar navigation items to template context.
    """
    return {
        'sidebar_items': get_sidebar_items(request)
    }