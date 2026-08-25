
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from .menu_builders import (
    SidebarItem,
    {%- if cookiecutter.has_blog == "y" %}
    build_blog_menu,
    {%- endif %}
    build_system_admin_menu,
)


def get_sidebar_items(request) -> list[SidebarItem]:
    """
    Generate the sidebar items based on the user's permissions and request path.
    """
    user = request.user

    sidebar = [
        SidebarItem(
            label=_("Dashboard"),
            icon="ti-dashboard",
            url=reverse_lazy("dashboard:home_page"),
            active=request.path == reverse_lazy("dashboard:home_page"),
        ),
        # TODO: conditionally build menus depending on app selection
        # SidebarItem(
        #     label=_("Jobs"),
        #     icon="ti-briefcase",
        #     url=reverse_lazy("dashboard:job_post_list"),
        #     active="/job-posts/" in request.path,
        #     permissions=["core.view_jobpost"],
        # ),
        # SidebarItem(
        #     label=_("Testimonials"),
        #     icon="ti-comment",
        #     url=reverse_lazy("dashboard:testimonial_list"),
        #     active="/testimonials/" in request.path,
        # ),
        # SidebarItem(
        #     label=_("Inquiries"),
        #     icon="ti-email",
        #     url=reverse_lazy("dashboard:inquiry_list"),
        #     active="/inquiries/" in request.path,
        #     permissions=["core.view_inquiry"],
        # ),
        {%- if cookiecutter.has_blog == "y" %}
        build_blog_menu(request),
        {%- endif %}
        build_system_admin_menu(request),
        # SidebarItem(
        #     label=_("Password Management"),
        #     icon="ti-info",
        #     url=reverse_lazy("password_update"),
        #     active="/accounts/" in request.path,
        # ),
    ]

    # Convert to dictionaries and filter visible items
    return [item.to_dict(user) for item in sidebar if item.is_visible(user)]
