from typing import Any

from django.contrib import admin
from django.core.exceptions import PermissionDenied, ValidationError
from django.urls import exceptions, reverse
from django.utils.html import format_html, format_html_join

TABLE_EMPTY_FIELD_DASH = "-"
USER_ACCOUNT_MODEL = 'login_useraccount'

class HTMLTagStringGenerators:
    @staticmethod
    def __build_attrs(kwargs: dict[str, Any]):
        """
        Takes a dictionary of attributes,
        sorts them alphabetically by attribute names.
        The purpose of this function is to facilitate the
        construction of HTML tags with dynamically generated attributes.

        :param kwargs: Dictionary of attributes attr_name=attr_value
        :return: HTML-safe formatted string containing the attributes in key=value style,
                separated by spaces.
        """
        return format_html_join(
            " ",
            '{}="{}"',
            ((k, v) for k, v in sorted(kwargs.items(), key=lambda x: x[0])),
        )

    @staticmethod
    def __check_args(valid_args: set, kwargs: dict[str, Any]) -> dict[str, Any]:
        """
        Checks the attributes specified are in the valid list of attributes.
        Because "class" is a python reserved keyword a trailing underscore can be added to
        allow support for this attribute. Use "class_" instead and the code automatically
        drops the underscore when rendered.

        :param valid_args: A set containing all value attribute names
        :param kwargs: dictionary of html attribute name and values.

        :return: corrected dictionary of attribute names and values where the trailing
        underscore has been dropped from the names.
        """
        # Strip trailing underscore for _class assuming it is specified.
        kwargs = {k.rstrip("_"): v for k, v in kwargs.items()}

        invalid_tags = set(kwargs).difference(valid_args)

        # remove any data-* tags as these are valid
        invalid_tags = {tag for tag in invalid_tags if not tag.startswith("data-")}

        if len(invalid_tags) > 0:
            attrs = ", ".join(sorted(invalid_tags))
            raise ValidationError(f"The following tag(s) are invalid: {attrs}")
        return kwargs

    @classmethod
    def a_tag(cls, *, value: str, **kwargs) -> str:
        """
        Returns a safe string containing the a-tag
        i.e.
        SafeString('<a class_="" href="" target="_blank">Value</a>')

        :param value: The value that is displayed on screen i.e. <a>{value}</a>
        :param kwargs: can be one of the arg names set below in valid_args
        :return: Safe string containing a-tag
        """
        # These are a list of HTML5 compatible attributes of the HTML 'a' tag taken from
        # https://www.w3schools.com/tags/tag_a.asp
        # The value attribute is the name of the link displayed on screen
        # i.e. <a>{value}</a>
        valid_args = {
            "href",
            "value",
            "download",
            "hreflang",
            "media",
            "ping",
            "referrerpolicy",
            "rel",
            "target",
            "type",
        }
        kwargs = cls.__check_args(valid_args, kwargs)
        return format_html("<a {}>{}</a>", cls.__build_attrs(kwargs), value)

    @classmethod
    def admin_url(cls, model_name: str, view_name: str, **kwargs):
        """
        Generate a dynamic django admin
        url based on arguments passed
        """
        try:
            obj_id = kwargs.pop("obj_id", None)
            url = reverse(f"admin:{model_name}_{view_name}", args=(obj_id,))
            return cls.a_tag(
                href=url,
                value=kwargs["value"],
                target=kwargs.get("target", "_blank"),
            )
        except KeyError:
            return TABLE_EMPTY_FIELD_DASH
        except exceptions.NoReverseMatch:
            return TABLE_EMPTY_FIELD_DASH


class UploadedByAdminMixin(admin.ModelAdmin):
    readonly_fields = ('uploaded_by',)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)

    def uploaded_by_link(self, obj):
        return HTMLTagStringGenerators.admin_url(
            obj_id=obj.uploaded_by_id,
            model_name=USER_ACCOUNT_MODEL,
            view_name='change',
            value=obj.uploaded_by,
        )

    uploaded_by_link.short_description = 'Uploaded By'


class ReadOnlyModelAdmin(admin.ModelAdmin):
    def changeform_view(
        self, request, object_id=None, form_url='', extra_context=None,
    ):
        extra_context = extra_context or {}
        if request.method == 'POST' and not extra_context.pop(
            'override_post_permission', False,
        ):
            raise PermissionDenied
        extra_context.setdefault('show_save_and_continue', False)
        extra_context.setdefault('show_save', False)
        return super().changeform_view(
            request, object_id, form_url, extra_context,
        )

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def get_readonly_fields(self, request, obj=None):
        del request
        return (
            list(self.readonly_fields)
            + [field.name for field in obj._meta.fields]
            + [field.name for field in obj._meta.many_to_many]
        )  # yapf: disable

    def has_add_permission(self, request, obj=None):
        del request, obj
        return False

    def has_delete_permission(self, request, obj=None):
        del request, obj
        return False

    def has_change_permission(self, request, obj=None):
        del request, obj
        return False
