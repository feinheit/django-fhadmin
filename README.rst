Django-FHAdmin
==============

Modifies the stock Django-Administration interface to fit our ideas a little
bit better.


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
