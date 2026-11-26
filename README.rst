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

Allows grouping of apps on the dashboard and offers the same view on each
admin page when clicking the main title of the Django admin interface.

App label entries without a matching app are ignored. A configuration example
follows:

.. code-block:: python

    from fhadmin import FHADMIN_GROUPS_REMAINING
    _ = lambda x: x

    FHADMIN_GROUPS = [
        (_('Main content'), ('page', 'medialibrary', 'blog')),
        (_('Modules'), ('links', FHADMIN_GROUPS_REMAINING)),
        (_('Preferences'), ('auth', 'rosetta', 'external', 'sites')),
    ]


The extension is activated by inserting ``fhadmin`` before
``django.contrib.admin`` in ``INSTALLED_APPS``.


Merging apps
------------

Merging apps is possible as follows:

.. code-block:: python

    FHADMIN_MERGE = {"accounts": "auth"}

This example moves all models from the ``accounts`` app to the ``auth``
heading. Entries where source and target do not exist are ignored.


Tests
-----

``tox`` runs the tests and takes Playwright screenshots of the main admin
pages in light and dark mode. They end up in
``tests/screenshots/django-<version>/``.
