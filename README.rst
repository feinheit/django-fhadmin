Django-FHAdmin
==============

Modifies the stock Django-Administration interface to fit our ideas a little
bit better.


Dashboard and global navigation extension
-----------------------------------------

Allows grouping of apps on the dashboard and offers the same view on each
admin page by sliding down the bar on top after a small delay when hovered.

Configuration example::

    from fhadmin import FHADMIN_GROUPS_REMAINING
    _ = lambda x: x

    FHADMIN_GROUPS_CONFIG = [
        (_('Main content'), {
            'apps': ('page', 'medialibrary', 'blog'),
            }),
        (_('Modules'), {
            'apps': ('links', FHADMIN_GROUPS_REMAINING),
            }),
        (_('Preferences'), {
            'apps': ('auth', 'rosetta', 'external', 'sites'),
            }),
        ]


The extension is activated by inserting ``fhadmin`` before
``django.contrib.admin`` in ``INSTALLED_APPS``.
