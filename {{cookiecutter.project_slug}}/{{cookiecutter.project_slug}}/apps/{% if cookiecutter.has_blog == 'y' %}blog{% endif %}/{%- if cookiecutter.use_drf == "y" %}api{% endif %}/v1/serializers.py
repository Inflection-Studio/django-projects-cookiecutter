from rest_framework import serializers
from taggit.serializers import TaggitSerializer, TagListSerializerField

from {{ cookiecutter.project_slug }}.apps.blog import models


class BaseContentSerializer(TaggitSerializer):
    tags = TagListSerializerField()
    published_at = serializers.ReadOnlyField()


class ArticleCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ArticleCategory
        fields = ("slug", "name")


class ArticleSerializer(serializers.ModelSerializer, BaseContentSerializer):
    category = ArticleCategorySerializer()

    class Meta:
        model = models.Blog
        fields = [
            "slug",
            "title",
            "body",
            "cover_image",
            "tags",
            "category",
            "created",
            "published_at",
        ]
