from decimal import Decimal

from django.utils.crypto import get_random_string
from django.utils.text import slugify


def unique_slug_generator(instance, new_slug: str = None, field_name: str = "name"):
    if new_slug is not None:
        slug = new_slug
    else:
        random_string = get_random_string(length=6)
        slug = slugify(f"{getattr(instance, field_name)} {random_string}")
    Klass = instance.__class__
    max_length = Klass._meta.get_field("slug").max_length
    slug = slug[:max_length]
    qs_exists = Klass.objects.filter(slug=slug).exists()

    if qs_exists:
        new_slug = f"{slug[:max_length - 5]}-{get_random_string(length=6)}"
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug


def get_average_review_rating(reviews) -> Decimal:
    total_reviews = reviews.count()
    if total_reviews > 0:
        total_rating = sum([review.rating for review in reviews])
        return total_rating / Decimal(total_reviews)
    return Decimal(0.0)
