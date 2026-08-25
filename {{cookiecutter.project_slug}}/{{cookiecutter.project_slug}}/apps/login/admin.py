from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _

User = get_user_model()


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    model = User
    list_display = (
        "id",
        {%- if cookiecutter.username_type == "username" %}
        "username",
        {%- endif %}
        "email",
        "first_name",
        "last_name",
        "is_active",
        "is_staff",
        "is_superuser",
    )
    list_filter = ("is_active", "is_staff", "is_superuser")
    search_fields = (
        {%- if cookiecutter.username_type == "username" %}
        "username",
        {%- endif %}
        "email",
        "first_name",
        "last_name",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    {%- if cookiecutter.username_type == "username" %}
                    "username",
                    {%- endif %}
                    "password",
                ),
            },
        ),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    ordering = ["id"]
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    {%- if cookiecutter.username_type == "username" %}
                    "username",
                    {%- endif %}
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )
