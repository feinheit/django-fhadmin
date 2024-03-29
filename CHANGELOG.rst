Change log
==========

`Next version`_
~~~~~~~~~~~~~~~

.. _Next version: https://github.com/feinheit/django-fhadmin/compare/2.2...main

- Added support for merging apps.
- Reinstated the support for filtering the dashboard by ``app_label``.
- Added an ``AppConfig`` class which automatically sets
  ``admin.site.enable_nav_sidebar = False``. The quickpanel replaces the
  sidebar.
- Minimally reduce the size of the triangle.
- Started raising an ``ImproperlyConfigured`` exception when encountering a
  ``FHADMIN_GROUPS`` configuration without ``FHADMIN_GROUPS_REMAINING``.


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
