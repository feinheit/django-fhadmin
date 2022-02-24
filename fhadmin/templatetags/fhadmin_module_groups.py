import operator
from functools import reduce

from django import template
from django.conf import settings
from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.text import capfirst
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


def fhadmin_group_list(admin_site, request):
    fhadmin_groups = getattr(settings, "FHADMIN_GROUPS", FHADMIN_GROUPS_DEFAULT)
    base_url = reverse("admin:index")

    # -- 8< --  copied from django.contrib.admin.sites.AdminSite.index
    app_dict = {}
    user = request.user
    for model, model_admin in admin_site._registry.items():
        app_label = model._meta.app_label
        has_module_perms = user.has_module_perms(app_label)

        if has_module_perms:
            perms = model_admin.get_model_perms(request)

            # Check whether user has any perm for this module.
            # If so, add the module to the model_list.
            if True in perms.values():
                model_dict = {
                    "name": capfirst(model._meta.verbose_name_plural),
                    "admin_url": base_url
                    + mark_safe(f"{app_label}/{model.__name__.lower()}/"),
                    "perms": perms,
                }
                if app_label in app_dict:
                    app_dict[app_label]["models"].append(model_dict)
                else:
                    app_dict[app_label] = {
                        "name": app_label.title(),
                        "app_url": base_url + app_label + "/",
                        "has_module_perms": has_module_perms,
                        "models": [model_dict],
                        "app_label": app_label,  # MK added this
                    }

    # Sort the apps alphabetically.
    app_list = sorted(app_dict.values(), key=lambda value: value["name"])

    # Sort the models alphabetically within each app.
    for app in app_list:
        app["models"] = sorted(app["models"], key=lambda value: value["name"])
    # -- 8< --  copied from django.contrib.admin.sites.AdminSite.index

    all_available = [app["app_label"] for app in app_list]
    all_configured = reduce(
        operator.add, (list(apps) for title, apps in fhadmin_groups), []
    )

    all_remains = [a for a in all_available if a not in all_configured]

    for title, apps in fhadmin_groups:
        group_apps = []
        for app in apps:
            if app == FHADMIN_GROUPS_REMAINING:
                group_apps.extend(app_dict[a] for a in all_remains if a in app_dict)
            elif app in app_dict:
                group_apps.append(app_dict[app])
            # else: Do nothing, ignore

        if group_apps:
            yield title, group_apps


class FHAdminGroupListNode(template.Node):
    def __init__(self, request):
        self.request = template.Variable(request)

    def render(self, context):
        request = self.request.resolve(context)
        context["group_list"] = fhadmin_group_list(admin.sites.site, request)
        return ""


def do_fhadmin_group_list(parser, token):
    """
    {% fhadmin_group_list request %}

    Creates a ``group_list`` variable in the current context.
    """

    tag_name, request = token.split_contents()
    return FHAdminGroupListNode(request)


register.tag("fhadmin_group_list", do_fhadmin_group_list)
