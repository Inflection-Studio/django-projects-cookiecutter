from dataclasses import dataclass, field
from typing import Optional

from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from .menu_builders import build_system_admin_menu

@dataclass
class SidebarItem:
    label: str
    url: str = "#"
    active: bool = False
    icon: str | None = None
    sub_menu: list["SidebarItem"] = field(default_factory=list)
    permissions: list[str] = field(default_factory=list)

    def is_visible(self, user) -> bool:
        """
        Check if the item is visible to the given user.
        """
        if not self.permissions:
            return True
        return user.has_perms(self.permissions)

    def to_dict(self, user) -> Optional[dict]:
        """
        Convert the sidebar item to a dictionary if visible to the user.
        """
        if not self.is_visible(user):
            return None
        return {
            "label": self.label,
            "icon": self.icon,
            "url": self.url,
            "active": self.active,
            "sub_menu": [
                sub_item.to_dict(user)
                for sub_item in self.sub_menu
                if sub_item.is_visible(user)
            ],
        }


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
        build_system_admin_menu(request),
        SidebarItem(
            label=_("Password Management"),
            icon="ti-info",
            url=reverse_lazy("password_update"),
            active="/accounts/" in request.path,
        ),
    ]

    # Convert to dictionaries and filter visible items
    return [item.to_dict(user) for item in sidebar if item.is_visible(user)]
