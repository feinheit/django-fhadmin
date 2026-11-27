from django.apps import apps
from django.conf import settings
from django.core import checks

from fhadmin import Box, Link
from fhadmin.groups import OLD_REMAINING, REMAINING


def _check_string(string, where):
    if string in {REMAINING, OLD_REMAINING}:
        return []
    try:
        if "." in string:
            apps.get_model(string)
        else:
            apps.get_app_config(string)
    except LookupError:
        return [
            checks.Warning(
                f"{where} refers to {string!r}, which is neither an installed app"
                " nor a model.",
                id="fhadmin.W001",
            )
        ]
    return []


def _check_entry(entry, where):
    if isinstance(entry, str):
        return _check_string(entry, where)
    if isinstance(entry, Link):
        return []
    if isinstance(entry, (Box, tuple, list)):
        errors = []
        for e in entry.entries if isinstance(entry, Box) else entry:
            if isinstance(e, str) and e in {REMAINING, OLD_REMAINING}:
                errors.append(
                    checks.Error(
                        f"{where}: '*' cannot be part of a box.", id="fhadmin.E002"
                    )
                )
            elif isinstance(e, (str, Link)):
                errors.extend(_check_entry(e, where))
            else:
                errors.append(
                    checks.Error(
                        f"{where}: a box contains {e!r}, only app labels, models"
                        " and links are allowed.",
                        id="fhadmin.E001",
                    )
                )
        return errors
    return [
        checks.Error(
            f"{where} contains {entry!r}, which is not a valid entry.",
            id="fhadmin.E001",
        )
    ]


def check_settings(app_configs, **kwargs):
    if not hasattr(settings, "FHADMIN_GROUPS"):
        config = {}
    else:
        config = settings.FHADMIN_GROUPS

    errors = []
    if isinstance(config, dict):
        items = config.items()
    else:
        errors.append(
            checks.Warning(
                "FHADMIN_GROUPS is a list of (title, entries) tuples.",
                hint="Use a dict mapping titles to lists of entries instead.",
                id="fhadmin.W002",
            )
        )
        items = config

    for title, entries in items:
        where = f"FHADMIN_GROUPS[{str(title)!r}]"
        if isinstance(entries, str):
            entries = [entries]
        for entry in entries:
            errors.extend(_check_entry(entry, where))

    if getattr(settings, "FHADMIN_MERGE", None):
        errors.append(
            checks.Warning(
                "FHADMIN_MERGE is deprecated.",
                hint=(
                    "Combine the apps in one box with a tuple entry in"
                    ' FHADMIN_GROUPS instead, e.g. ("auth", "accounts").'
                ),
                id="fhadmin.W003",
            )
        )
    return errors
