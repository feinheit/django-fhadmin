from content_editor.admin import ContentEditor, ContentEditorInline
from django.contrib import admin, messages

from testapp import models


@admin.register(models.Model)
class ParentAdmin(admin.ModelAdmin):
    list_display = ["title"]


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ["name"]


class ArticleLinkInline(admin.TabularInline):
    model = models.ArticleLink
    extra = 1


class ArticleNoteInline(admin.StackedInline):
    model = models.ArticleNote
    extra = 1


@admin.action(description="Mark selected articles as published")
def make_published(modeladmin, request, queryset):
    count = queryset.update(status="published")
    messages.success(request, f"{count} articles were marked as published.")


@admin.register(models.Article)
class ArticleAdmin(admin.ModelAdmin):
    actions = [make_published]
    autocomplete_fields = ["category"]
    date_hierarchy = "published_on"
    fieldsets = [
        (None, {"fields": ["title", ("category", "slug"), "lead"]}),
        (
            "Publication",
            {
                "fields": [
                    "status",
                    "is_featured",
                    ("published_on", "updated_at"),
                    "lead_length",
                ]
            },
        ),
    ]
    inlines = [ArticleLinkInline, ArticleNoteInline]
    list_display = ["title", "category", "status", "is_featured", "published_on"]
    list_editable = ["status"]
    list_filter = ["status", "is_featured", "category"]
    prepopulated_fields = {"slug": ["title"]}
    radio_fields = {"status": admin.VERTICAL}
    readonly_fields = ["lead_length"]
    search_fields = ["title"]

    @admin.display(description="Lead length")
    def lead_length(self, obj):
        return f"{len(obj.lead)} characters"


@admin.register(models.Page)
class PageAdmin(ContentEditor):
    inlines = [
        ContentEditorInline.create(model=models.RichText),
        ContentEditorInline.create(model=models.Container),
    ]
