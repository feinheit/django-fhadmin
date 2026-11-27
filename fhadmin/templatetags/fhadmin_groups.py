from django import template
from django.contrib import admin

from fhadmin.groups import generate_group_list


register = template.Library()

__all__ = ["generate_group_list"]


@register.simple_tag(takes_context=True)
def fhadmin_group_list(context, request):
    only_app_label = None
    if context.get("apply_app_label_filtering"):
        only_app_label = context.get("app_label")
    return generate_group_list(admin.sites.site, request, only_app_label=only_app_label)
