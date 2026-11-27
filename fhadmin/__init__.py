__version__ = "3.1.0"

# Deprecated alias, use "*" instead
FHADMIN_GROUPS_REMAINING = "*"


class Box:
    """A box on the dashboard showing the models and links of several entries

    ``title`` defaults to the name of the first app in ``entries``.
    """

    def __init__(self, title, entries):
        self.title = title
        self.entries = tuple(entries)

    def __repr__(self):
        return f"Box({self.title!r}, {list(self.entries)!r})"


class Link:
    """A link to any admin page, e.g. a custom view, inside a box

    ``url`` is the name of a URL pattern or a URL. ``permission`` is a
    permission name such as ``"blog.view_article"`` or a callable receiving
    the request; the link is only shown when it passes.
    """

    def __init__(self, name, url, *, permission=None):
        self.name = name
        self.url = url
        self.permission = permission

    def __repr__(self):
        return f"Link({self.name!r}, {self.url!r})"
