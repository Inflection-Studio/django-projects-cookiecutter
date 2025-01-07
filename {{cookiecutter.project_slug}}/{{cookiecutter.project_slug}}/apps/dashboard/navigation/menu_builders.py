from django.urls import reverse_lazy
from .sidebar import SidebarItem
from .constants import *

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
                label="Articles",
                url=reverse_lazy("dashboard:article_list")
            ),
            SidebarItem(
                label="Categories",
                url=reverse_lazy("dashboard:category_list")
            ),
        ]
    )


def build_system_admin_menu(request) -> SidebarItem:
    return SidebarItem(
            label=LABEL_SYSTEM_ADMIN,
            icon=ICON_SETTINGS,
            active="users" in request.path,
            permissions=PERM_VIEW_USER,
            sub_menu=[
                SidebarItem(
                    label="All Staff", url=reverse_lazy("dashboard:login:staff_list")
                ),
                SidebarItem(
                    label="Add Staff", url=reverse_lazy("dashboard:login:staff_create")
                ),
            ],
        ),
