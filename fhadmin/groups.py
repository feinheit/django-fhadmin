"""Grouping of the admin's apps and models on the dashboard and the quickpanel

``FHADMIN_GROUPS`` maps group titles to lists of entries. The titles are
translated when rendering; mark them with ``gettext_noop``, lazy translations
cannot be used as dict keys in settings. An entry is

- an app label (``"blog"``): the app's models which aren't listed elsewhere
  with their own ``app_label.Model`` entry,
- a model (``"auth.User"``),
- ``"*"``: every app with models not listed anywhere else, one box each,
- a tuple of app labels, models and links, shown in one box under the first
  app's name, or a ``Box`` with a title of its own; the models are sorted by
  name, the links follow in the configured order,
- a ``Link`` to any admin page, shown in a box of its own.

Without ``"*"``, everything not listed ends up in an "Other" group at the end.
"""

from django.conf import settings
from django.urls import NoReverseMatch, reverse
from django.utils.translation import gettext, gettext_noop

from fhadmin import Box, Link


REMAINING = "*"
# The value of FHADMIN_GROUPS_REMAINING before 4.0
OLD_REMAINING = "REMAINING"

# Dict keys are hashed, which would evaluate lazy translations while the
# settings are loaded. Titles are therefore marked with gettext_noop and
# translated when rendering.
FHADMIN_GROUPS_DEFAULT = {
    gettext_noop("Modules"): [REMAINING],
    gettext_noop("Preferences"): ["auth", "sites"],
}


def configured_groups():
    """``[(title, [entry])]`` with every entry a string or a ``Box``"""
    config = getattr(settings, "FHADMIN_GROUPS", FHADMIN_GROUPS_DEFAULT)
    # The list of (title, entries) tuples is deprecated, see checks.py
    items = config.items() if isinstance(config, dict) else config
    groups = []
    for title, entries in items:
        if isinstance(entries, (str, Box, Link)):
            entries = [entries]
        groups.append((title, [_normalize(entry) for entry in entries]))
    return groups


def _normalize(entry):
    if entry == OLD_REMAINING:
        return REMAINING
    if isinstance(entry, (tuple, list)):
        return Box(None, entry)
    if isinstance(entry, Link):
        return Box(None, [entry])
    return entry


def _strings(entry):
    entries = entry.entries if isinstance(entry, Box) else [entry]
    return [e for e in entries if isinstance(e, str)]


def _link_row(link, request):
    if callable(link.permission):
        if not link.permission(request):
            return None
    elif link.permission and not request.user.has_perm(link.permission):
        return None
    try:
        url = reverse(link.url)
    except NoReverseMatch:
        url = link.url
    return {
        "name": link.name,
        "object_name": "link",
        "perms": {"view": True},
        "admin_url": url,
        "add_url": None,
        "view_only": True,
    }


def generate_group_list(admin_site, request, *, only_app_label=None):
    """Yields ``(title, app_list)`` with ``app_list`` like Django's"""
    apps = {app["app_label"]: app for app in admin_site.get_app_list(request)}

    # Deprecated, a tuple entry does the same
    for app_label, merge_into in getattr(settings, "FHADMIN_MERGE", {}).items():
        if app_label in apps and merge_into in apps:
            apps[merge_into] = apps[merge_into] | {
                "models": sorted(
                    apps[merge_into]["models"] + apps.pop(app_label)["models"],
                    key=lambda row: row["name"],
                )
            }

    models = {}
    for app in apps.values():
        for model in app["models"]:
            models[model["model"]._meta.label_lower] = app, model

    groups = configured_groups()
    listed = {
        string.lower()
        for _title, entries in groups
        for entry in entries
        for string in _strings(entry)
    }

    def rows(string):
        """``(app, [model rows])`` of an app label or a model entry"""
        string = string.lower()
        if "." in string:
            if string in models:
                app, model = models[string]
                return app, [model]
            return None, []
        if app := apps.get(string):
            return app, [
                model
                for model in app["models"]
                if model["model"]._meta.label_lower not in listed
            ]
        return None, []

    def box(entry):
        if isinstance(entry, str):
            app, app_models = rows(entry)
            return app and app_models and app | {"models": app_models}
        if not isinstance(entry, Box):
            return None  # Reported by the system check

        first_app, box_models, links = None, [], []
        for e in entry.entries:
            if isinstance(e, Link):
                if row := _link_row(e, request):
                    links.append(row)
            elif isinstance(e, str):
                app, app_models = rows(e)
                first_app = first_app or app
                box_models.extend(app_models)
        # Sorted by name like Django sorts the models of an app, the links
        # follow in the configured order
        box_models = sorted(box_models, key=lambda row: str(row["name"])) + links
        if not box_models:
            return None
        if first_app:
            return first_app | {
                "name": entry.title or first_app["name"],
                "models": box_models,
            }
        return {
            "name": entry.title or box_models[0]["name"],
            "app_label": "fhadmin",
            "app_url": box_models[0]["admin_url"],
            "has_module_perms": True,
            "models": box_models,
        }

    def remaining():
        return [
            app | {"models": app_models}
            for app_label in apps
            if app_label not in listed
            for app, app_models in [rows(app_label)]
            if app_models
        ]

    has_remaining = any(REMAINING in entries for _title, entries in groups)
    if not has_remaining:
        groups = [*groups, (gettext_noop("Other"), [REMAINING])]

    for title, entries in groups:
        boxes = []
        for entry in entries:
            if entry == REMAINING:
                boxes.extend(remaining())
            elif b := box(entry):
                boxes.append(b)
        if only_app_label is not None:
            boxes = [b for b in boxes if b["app_label"] == only_app_label]
        if boxes:
            yield (gettext(title) if isinstance(title, str) else title), boxes
