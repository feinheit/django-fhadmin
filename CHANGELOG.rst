Change log
==========

Next version
~~~~~~~~~~~~

3.2 (2026-11-27)
~~~~~~~~~~~~~~~~

- ``FHADMIN_GROUPS`` is now a dict mapping group titles to lists of entries.
  Entries can be app labels, single models (``"auth.User"``), ``"*"`` for
  everything not listed, tuples showing several apps and models in one box,
  ``Box`` objects with a title of their own and ``Link`` objects pointing to
  any admin page, e.g. custom views, optionally only for users with a
  permission. Boxes sort their models by name and show the links last. Mark the titles with ``gettext_noop``, fhadmin translates them
  when rendering; lazy translations cannot be dict keys in settings.
- Leaving out ``"*"`` no longer raises ``ImproperlyConfigured`` when the
  dashboard renders; everything not listed ends up in an "Other" group.
- Added system checks for unknown app labels and models (``fhadmin.W001``)
  and invalid entries (``fhadmin.E001``, ``fhadmin.E002``).
- The default groups only list ``auth`` and ``sites`` instead of our own apps.
- Deprecated the list of ``(title, entries)`` tuples (``fhadmin.W002``),
  ``FHADMIN_GROUPS_REMAINING`` (now an alias for ``"*"``) and
  ``FHADMIN_MERGE`` (``fhadmin.W003``), use tuple entries instead.

3.1 (2026-11-26)
~~~~~~~~~~~~~~~~

- Django 6.1 stacks label, help text, errors and input of every field. On
  screens at least 768px wide the label moves back into a column of its own,
  with errors, input and help text next to it. Further fields on a shared
  line only take as much room as their label. Inputs and selects keep their
  own width, wrappers such as rich text editors fill the column. Fields with
  an empty label (which django-prose-editor and django-json-schema-editor
  hide) use the whole width. Django 5.2 and 6.0 are unaffected.
- The submit row no longer sticks to the bottom of the window, it jumped
  around while scrolling. On small screens its buttons wrap instead of
  stacking.
- Long labels of objects chosen in raw ID fields wrap instead of overflowing.
- Fields fit into their row on small screens. Django's ``responsive.css``
  and django-content-editor size them by the viewport, which left them
  sticking out of modules, inlines and nested plugins.

3.0 (2026-11-26)
~~~~~~~~~~~~~~~~

fhadmin is now an admin theme. Installing it restyles every admin page; there
is no setting to turn the theme off. Django's admin templates stay as they
are, the theme only sets Django's admin CSS variables and adds component rules
for Django's own class names (``fhadmin/theme.css``).

- Added light and dark tokens for Django's admin variables, following
  ``prefers-color-scheme`` and Django's theme toggle (``html[data-theme]``).
- Added the shared extension variables ``--admin-radius`` and
  ``--admin-border-strong``, which django-content-editor, django-prose-editor
  and others use with fallbacks.
- Restyled the header, breadcrumbs, module captions (no more coloured caption
  bars), buttons, input focus rings, change list, filters, actions, messages,
  inlines and the login page. The submit row sticks to the bottom of the
  window on long forms; only the "Save" button is filled.
- The quickpanel toggle can be used with the keyboard. Its triangle moved from
  ``#site-name::after`` to ``#branding::after``, so ``#site-name::after`` is
  free again, e.g. for the environment name.
- Dropped support for Django < 5.2 and Python < 3.12. Supported are Django
  5.2, 6.0 and 6.1.
- Replaced the test runner with pytest and added Playwright screenshots of
  the main admin pages in light and dark mode, including a content-editor
  and a prose-editor field.

Migration notes:

- Everything looks different: green header, quiet module headings, outlined
  secondary buttons, a sticky submit row, stronger input borders.
- Environment colours keep working. Override ``--primary``, ``--secondary``
  and ``--accent``; the header, buttons, links and selected rows are derived
  from them. The stylesheets are loaded at the start of the ``extrahead``
  block, so overrides in ``admin/base.html``'s ``extrahead`` (after
  ``{{ block.super }}``) win. Use ``html[data-theme], :root`` instead of
  ``:root`` as selector so the override also wins when users chose light or
  dark mode explicitly.
- Projects with their own ``admin/base_site.html`` have to extend fhadmin's
  (``{% extends "admin/base_site.html" %}`` as the first app template found
  after the project's) or include ``fhadmin/theme.css`` themselves.


2.4 (2026-06-15)
~~~~~~~~~~~~~~~~

- Added official support for Django 5.2, 6.0, Python 3.13, 3.14.
- Fix a styling issue where all links were underlined.
- Converted the package to use modern packaging standards.


2.3 (2024-09-24)
~~~~~~~~~~~~~~~~

- Added support for merging apps.
- Reinstated the support for filtering the dashboard by ``app_label``.
- Added an ``AppConfig`` class which automatically sets
  ``admin.site.enable_nav_sidebar = False``. The quickpanel replaces the
  sidebar.
- Minimally reduce the size of the triangle.
- Started raising an ``ImproperlyConfigured`` exception when encountering a
  ``FHADMIN_GROUPS`` configuration without ``FHADMIN_GROUPS_REMAINING``.
- Added Python 3.12, Django 4.2, Django 5.1.
- Tweaked the styles a bit.
- Avoided navigating to the admin index when clicking the main title, expand
  the panel instead.


`2.2`_ (2022-02-24)
~~~~~~~~~~~~~~~~~~~

.. _2.2: https://github.com/feinheit/django-fhadmin/compare/2.1...2.2

- Added a testsuite and CI using GitHub actions.
- Simplified the implementation while taking advantage of new functionality in
  Django.
- Made the quickpanel available on the index page too by removing useless
  animations and implementing the JavaScript without jQuery.


`2.1`_ (2022-02-24)
~~~~~~~~~~~~~~~~~~~

.. _2.1: https://github.com/feinheit/django-fhadmin/compare/2.0...2.1

- Simplified the data structure of the groups configuration.


`2.0`_ (2022-02-24)
~~~~~~~~~~~~~~~~~~~

.. _2.0: https://github.com/feinheit/django-fhadmin/compare/532122b...2.0

- Dropped support for Django < 3.2, Python < 3.8.
- Fixed and reduced the CSS code.
- Amended the default module groups a bit.


`1.4.2`_ (2018-11-26)
~~~~~~~~~~~~~~~~~~~~~

.. _1.4.2: https://github.com/feinheit/django-fhadmin/commit/532122b

- No release notes.
