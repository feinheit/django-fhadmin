Django-FHAdmin
==============

Modifies the stock Django-Administration interface to fit our ideas a little
bit better: an admin theme and a grouped dashboard.


Theme
-----

Installing fhadmin restyles the admin. The theme keeps Django's templates and
only sets Django's admin CSS variables (light and dark) plus a small set of
component rules, so third-party apps which use the variables follow along.

It also sets two shared variables for other packages, which use them with a
fallback:

- ``--admin-radius``: corner radius
- ``--admin-border-strong``: borders which have to be visible to tell
  components apart (at least 3:1 contrast)

Environment colours
~~~~~~~~~~~~~~~~~~~

The brand colours are ``--primary``, ``--secondary`` (header, default button)
and ``--accent`` (site name); everything else is derived from them. To
distinguish environments, override them in ``admin/base.html``:

.. code-block:: html+django

    {% extends "admin/base.html" %}

    {% block extrahead %}{{ block.super }}
    {% if ENVIRONMENT == "production" %}
    <style>
      html[data-theme], :root {
        --primary: #aa0000;
        --secondary: #810000;
        --accent: yellow;
      }
    </style>
    {% endif %}
    {% endblock %}

The ``html[data-theme]`` part makes the override win even when somebody
chose light or dark mode explicitly using Django's theme toggle.


Dashboard and global navigation extension
-----------------------------------------

Groups the apps and models on the dashboard and offers the same view on each
admin page when clicking the main title of the Django admin interface.

``FHADMIN_GROUPS`` maps group titles to lists of entries:

.. code-block:: python

    from django.utils.translation import gettext_lazy as _, gettext_noop

    from fhadmin import Box, Link

    FHADMIN_GROUPS = {
        gettext_noop("Content"): ["pages", "medialibrary", "blog"],
        gettext_noop("People"): [("little_auth.User", "auth.Group"), "accounts"],
        gettext_noop("Preferences"): [
            "sites",
            "*",
            Box(
                _("Reports"),
                [
                    "blog.Comment",
                    Link(
                        _("Broken links"),
                        "admin:blog_article_broken_links",
                        permission="blog.view_article",
                    ),
                ],
            ),
        ],
    }

An entry is one of:

- An app label (``"blog"``): the app's models, except those listed elsewhere
  with an entry of their own.
- A model (``"auth.Group"``). More specific entries win: the rest of the
  ``auth`` app stays wherever ``"auth"`` is listed.
- ``"*"``: every app whose models aren't listed anywhere, each in its own box.
  Without ``"*"``, those end up in an "Other" group at the end.
- A tuple of app labels, models and links, shown in one box under the first
  app's name, or a ``Box`` with a title of its own. The models are sorted by
  name like within an app, the links follow in the configured order.
- A ``Link`` to any admin page, e.g. a custom view. ``url`` is the name of a
  URL pattern or a URL; ``permission`` is a permission name or a callable
  receiving the request, the link is only shown when it passes.

The titles are dict keys, and hashing a lazy translation would evaluate it
while the settings are loaded. Mark them with ``gettext_noop`` instead;
fhadmin translates them when rendering. Box titles and link names are no keys
and may be lazy.

A system check warns about app labels and models which don't exist and
reports invalid entries when Django starts.

The extension is activated by inserting ``fhadmin`` before
``django.contrib.admin`` in ``INSTALLED_APPS``.

The previous format, a list of ``(title, entries)`` tuples with
``FHADMIN_GROUPS_REMAINING`` instead of ``"*"``, still works but is
deprecated, as is ``FHADMIN_MERGE`` (``{"accounts": "auth"}`` showed the
models of ``accounts`` under the ``auth`` heading; use a tuple entry such as
``("auth", "accounts")`` instead).


Tests
-----

``tox`` runs the tests and takes Playwright screenshots of the main admin
pages in light and dark mode. They end up in
``tests/screenshots/django-<version>/``.
