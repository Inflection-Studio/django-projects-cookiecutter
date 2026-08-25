from django.utils.functional import SimpleLazyObject

from {{ cookiecutter.project_slug}}.apps.blog.models import Blog

from .utils import get_model_publication_analytics

article_analytics = SimpleLazyObject(
    lambda: get_model_publication_analytics(model=Blog),
)
