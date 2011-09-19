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


The extension is activated by overriding both ``admin/base_site.html`` for the
slide-down navigation and ``admin/index.html`` for the dashboard, and adding
``fhadmin`` to ``INSTALLED_APPS`` so that the template tags and static files
are found.

``admin/base_site.html``::

    {% extends "admin/base.html" %}
    {% load i18n %}

    {% block extrahead %}
    <link rel="stylesheet" type="text/css" href="{{ STATIC_URL }}fhadmin/fhadmin.css" />
    {% endblock %}

    {% block title %}{{ title }} | {% trans 'Django site admin' %}{% endblock %}

    {% block branding %}
    <h1 id="site-name">{% trans 'Django administration' %}</h1>
    {% endblock %}

    {% block nav-global %}
    <div id="quickpanel">
        {% include "admin/group_list.html" %}
        <br style="clear:both" />
    </div>
    {% endblock %}

``admin/index.html``::

    {% extends "admin/base_site.html" %}
    {% load i18n admin_static %}

    {% block extrastyle %}{{ block.super }}<link rel="stylesheet" type="text/css" href="{% static "admin/css/dashboard.css" %}" />{% endblock %}

    {% block coltype %}colMS{% endblock %}

    {% block bodyclass %}dashboard{% endblock %}

    {% block breadcrumbs %}{% endblock %}

    {% block content %}
    <div id="content-main">
        {% include "admin/group_list.html" %}
        <br style="clear:left" />
    </div>
    {% endblock %}

    {% block sidebar %}
    <div id="content-related">
        <div class="module" id="recent-actions-module">
            <h2>{% trans 'Recent Actions' %}</h2>
            <h3>{% trans 'My Actions' %}</h3>
                {% load log %}
                {% get_admin_log 10 as admin_log for_user user %}
                {% if not admin_log %}
                <p>{% trans 'None available' %}</p>
                {% else %}
                <ul class="actionlist">
                {% for entry in admin_log %}
                <li class="{% if entry.is_addition %}addlink{% endif %}{% if entry.is_change %}changelink{% endif %}{% if entry.is_deletion %}deletelink{% endif %}">
                    {% if entry.is_deletion %}
                        {{ entry.object_repr }}
                    {% else %}
                        <a href="{{ entry.get_admin_url }}">{{ entry.object_repr }}</a>
                    {% endif %}
                    <br/>
                    {% if entry.content_type %}
                        <span class="mini quiet">{% filter capfirst %}{% trans entry.content_type.name %}{% endfilter %}</span>
                    {% else %}
                        <span class="mini quiet">{% trans 'Unknown content' %}</span>
                    {% endif %}
                </li>
                {% endfor %}
                </ul>
                {% endif %}
        </div>
    </div>
    {% endblock %}
