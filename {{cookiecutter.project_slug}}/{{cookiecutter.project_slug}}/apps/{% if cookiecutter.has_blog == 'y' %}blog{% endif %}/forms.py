from django import forms
from tinymce.widgets import TinyMCE

from {{ cookiecutter.project_slug }}.apps.blog import models


class BaseContentForm(forms.ModelForm):
    body = forms.CharField(widget=TinyMCE())


class ArticleForm(BaseContentForm):
    class Meta:
        model = models.Blog
        fields = ["title", "category", "body", "tags", "cover_image"]
