import operator
from functools import reduce

from django import template
from django.conf import settings
from django.contrib import admin
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import gettext_lazy as _

from fhadmin import FHADMIN_GROUPS_REMAINING


register = template.Library()


FHADMIN_GROUPS_DEFAULT = [
    (
        _("Main content"),
        (
            "page",
            "medialibrary",
            "elephantblog",
            "pages",
            "articles",
            "cabinet",
        ),
    ),
    (
        _("Modules"),
        (
            "gallery",
            "agenda",
            "links",
            FHADMIN_GROUPS_REMAINING,
        ),
    ),
    (
        _("Preferences"),
        (
            "auth",
            "little_auth",
            "accounts",
            "admin_sso",
            "sites",
            "pinging",
            "feincms3_cookiecontrol",
            "feincms3_sites",
            "simple_redirects",
        ),
    ),
    (
        _("Collections"),
        (
            "external",
            "sharing",
            "newsletter",
            "form_designer",
        ),
    ),
]


def generate_group_list(admin_site, request, *, only_app_label=None):
    app_dict = {a["app_label"]: a for a in admin_site.get_app_list(request)}

    if merge := getattr(settings, "FHADMIN_MERGE", {}):
        for app_label, merge_into in merge.items():
            if app_label in app_dict and merge_into in app_dict:
                app_dict[merge_into]["models"] = sorted(
                    app_dict[merge_into]["models"] + app_dict.pop(app_label)["models"],
                    key=lambda row: row["name"],
                )

    if only_app_label is not None:
        for key in list(app_dict):
            if key != only_app_label:
                app_dict.pop(key)

    fhadmin_groups = getattr(settings, "FHADMIN_GROUPS", FHADMIN_GROUPS_DEFAULT)
    all_configured = reduce(
        operator.or_, (set(apps) for title, apps in fhadmin_groups), set()
    )

    seen_remaining = False
    for title, apps in fhadmin_groups:
        group_apps = []
        for app in apps:
            if app == FHADMIN_GROUPS_REMAINING:
                group_apps.extend(
                    a for a in app_dict.values() if a["app_label"] not in all_configured
                )
                seen_remaining = True
            elif app in app_dict:
                group_apps.append(app_dict[app])

        if group_apps:
            yield title, group_apps

    if not seen_remaining:
        raise ImproperlyConfigured(
            "Your FHADMIN_GROUPS override is missing FHADMIN_GROUPS_REMAINING."
        )


@register.simple_tag(takes_context=True)
def fhadmin_group_list(context, request):
    only_app_label = None
    if context.get("apply_app_label_filtering"):
        only_app_label = context.get("app_label")
    return generate_group_list(admin.sites.site, request, only_app_label=only_app_label)
