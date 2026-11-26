from content_editor.models import Region, create_plugin_base
from django.db import models
from django_prose_editor.fields import ProseEditorField


class Model(models.Model):
    title = models.CharField(max_length=100)


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Article(models.Model):
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("review", "In review"),
        ("published", "Published"),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(help_text="Used in the URL of the article.")
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    is_featured = models.BooleanField(default=False)
    published_on = models.DateField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    lead = ProseEditorField(
        extensions={
            "Bold": True,
            "Italic": True,
            "Link": True,
            "BulletList": True,
            "ListItem": True,
        },
        blank=True,
    )

    def __str__(self):
        return self.title


class ArticleLink(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    url = models.URLField()

    def __str__(self):
        return self.title


class ArticleNote(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    author = models.CharField(max_length=100)
    note = models.TextField()

    def __str__(self):
        return self.author


class Page(models.Model):
    title = models.CharField(max_length=200)

    regions = [
        Region(key="main", title="Main"),
        Region(key="sidebar", title="Sidebar"),
    ]

    def __str__(self):
        return self.title


PagePlugin = create_plugin_base(Page)


class RichText(PagePlugin):
    text = ProseEditorField(
        extensions={
            "Bold": True,
            "Italic": True,
            "Link": True,
            "BulletList": True,
            "ListItem": True,
            "Heading": {"levels": [2, 3]},
        },
        blank=True,
    )

    class Meta:
        verbose_name = "rich text"

    def __str__(self):
        return self.text[:40]


class Container(PagePlugin):
    container = True

    title = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.title
