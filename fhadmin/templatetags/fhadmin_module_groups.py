import operator
from functools import reduce

from django import template
from django.conf import settings
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from fhadmin import FHADMIN_GROUPS_REMAINING


register = template.Library()


FHADMIN_GROUPS_DEFAULT = [
    (
        _("Main content"),
        ("page", "medialibrary", "elephantblog", "pages", "articles"),
    ),
    (
        _("Modules"),
        ("gallery", "agenda", "links", FHADMIN_GROUPS_REMAINING),
    ),
    (
        _("Preferences"),
        (
            "auth",
            "little_auth",
            "accounts",
            "sites",
            "pinging",
            "feincms3_cookiecontrol",
            "feincms3_sites",
        ),
    ),
    (
        _("Collections"),
        ("external", "sharing", "newsletter", "form_designer"),
    ),
]


def generate_group_list(admin_site, request):
    app_list = admin_site.get_app_list(request)
    app_dict = {a["app_label"]: a for a in app_list}

    fhadmin_groups = getattr(settings, "FHADMIN_GROUPS", FHADMIN_GROUPS_DEFAULT)
    all_configured = reduce(
        operator.or_, (set(apps) for title, apps in fhadmin_groups), set()
    )

    for title, apps in fhadmin_groups:
        group_apps = []
        for app in apps:
            if app == FHADMIN_GROUPS_REMAINING:
                group_apps.extend(
                    a for a in app_list if a["app_label"] not in all_configured
                )
            elif app in app_dict:
                group_apps.append(app_dict[app])

        if group_apps:
            yield title, group_apps


@register.simple_tag(takes_context=True)
def fhadmin_group_list(context, request):
    context["group_list"] = list(generate_group_list(admin.sites.site, request))
    return ""
