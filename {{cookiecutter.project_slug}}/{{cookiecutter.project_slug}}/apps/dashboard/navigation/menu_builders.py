from dataclasses import dataclass, field

from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from .constants import (
    ICON_BLOG,
    ICON_SETTINGS,
    LABEL_BLOG,
    LABEL_SYSTEM_ADMIN,
    PERM_VIEW_USER,
)


@dataclass
class SidebarItem:
    label: str
    url: str = "#"
    active: bool = False
    icon: str | None = None
    sub_menu: list[SidebarItem] = field(default_factory=list)
    permissions: list[str] = field(default_factory=list)

    def is_visible(self, user) -> bool:
        """
        Check if the item is visible to the given user.
        """
        if not self.permissions:
            return True
        return user.has_perms(self.permissions)

    def to_dict(self, user) -> dict | None:
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


def build_blog_menu(request) -> SidebarItem:
    """
    Build the blog section of the sidebar menu.
    """
    return SidebarItem(
        label=LABEL_BLOG,
        icon=ICON_BLOG,
        active="/articles/" in request.path,
        sub_menu=[
            SidebarItem(
                label=_("Categories"),
                url=reverse_lazy("dashboard:articles:category_list"),
            ),
            SidebarItem(
                label=_("Articles"),
                url=reverse_lazy("dashboard:articles:article_list"),
            ),
            SidebarItem(
                label=_("Add Article"),
                url=reverse_lazy("dashboard:articles:article_list"),
            ),
        ],
    )


def build_system_admin_menu(request) -> SidebarItem:
    return SidebarItem(
        label=LABEL_SYSTEM_ADMIN,
        icon=ICON_SETTINGS,
        active="users" in request.path,
        permissions=[PERM_VIEW_USER],
        sub_menu=[
            SidebarItem(
                label=_("All Staff"),
                url=reverse_lazy("dashboard:login:staff_list"),
            ),
            SidebarItem(
                label=_("Add Staff"),
                url=reverse_lazy("dashboard:login:staff_create"),
            ),
        ],
    )
