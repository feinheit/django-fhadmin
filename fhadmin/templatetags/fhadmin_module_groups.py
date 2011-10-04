import operator

from django import template
from django.conf import settings
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.text import capfirst
from django.utils.translation import ugettext as _, ugettext_lazy

from fhadmin import FHADMIN_GROUPS_REMAINING

register = template.Library()


FHADMIN_GROUPS_CONFIG = [
    (ugettext_lazy('Main content'), {
        'apps': ('page', 'medialibrary', 'elephantblog'),
        }),
    (ugettext_lazy('Modules'), {
        'apps': ('gallery', 'agenda', 'links', FHADMIN_GROUPS_REMAINING),
        }),
    (ugettext_lazy('Preferences'), {
        'apps': ('auth', 'sites', 'pinging'),
        }),
    (ugettext_lazy('Collections'), {
        'apps': ('external', 'sharing', 'newsletter', 'form_designer'),
        }),
    ]

FHADMIN_GROUPS_CONFIG = getattr(settings, 'FHADMIN_GROUPS_CONFIG',
    FHADMIN_GROUPS_CONFIG)


def fhadmin_group_list(admin_site, request):
    base_url = reverse('admin:index')

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
                    'name': capfirst(model._meta.verbose_name_plural),
                    'admin_url': base_url + mark_safe('%s/%s/' % (app_label, model.__name__.lower())),
                    'perms': perms,
                }
                if app_label in app_dict:
                    app_dict[app_label]['models'].append(model_dict)
                else:
                    app_dict[app_label] = {
                        'name': app_label.title(),
                        'app_url': base_url + app_label + '/',
                        'has_module_perms': has_module_perms,
                        'models': [model_dict],
                        'app_label': app_label, # MK added this
                    }

    # Sort the apps alphabetically.
    app_list = app_dict.values()
    app_list.sort(lambda x, y: cmp(x['name'], y['name']))

    # Sort the models alphabetically within each app.
    for app in app_list:
        app['models'].sort(lambda x, y: cmp(x['name'], y['name']))
    # -- 8< --  copied from django.contrib.admin.sites.AdminSite.index

    all_available = [app['app_label'] for app in app_list]
    all_configured = reduce(operator.add, (list(v['apps']) for k, v in FHADMIN_GROUPS_CONFIG), [])

    all_remains = [a for a in all_available if a not in all_configured]

    for group_title, group in FHADMIN_GROUPS_CONFIG:
        apps = []
        for app in group['apps']:
            if app == FHADMIN_GROUPS_REMAINING:
                apps.extend(app_dict[a] for a in all_remains if a in app_dict)
            elif app in app_dict:
                apps.append(app_dict[app])
            # else: Do nothing, ignore

        if apps:
            yield group_title, apps


class FHAdminGroupListNode(template.Node):
    def __init__(self, request):
        self.request = template.Variable(request)

    def render(self, context):
        request = self.request.resolve(context)
        context['group_list'] = fhadmin_group_list(admin.sites.site, request)
        return u''


def do_fhadmin_group_list(parser, token):
    """
    {% fhadmin_group_list request %}

    Creates a ``group_list`` variable in the current context.
    """

    tag_name, request = token.split_contents()
    return FHAdminGroupListNode(request)

register.tag('fhadmin_group_list', do_fhadmin_group_list)
