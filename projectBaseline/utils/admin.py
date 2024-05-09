from typing import Any

from django.core.exceptions import ValidationError
from django.urls import exceptions, reverse
from django.utils.html import format_html, format_html_join

TABLE_EMPTY_FIELD_DASH = "-"


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
