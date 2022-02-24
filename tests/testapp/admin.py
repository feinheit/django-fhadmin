from django.contrib import admin
from testapp import models


@admin.register(models.Model)
class ParentAdmin(admin.ModelAdmin):
    list_display = ["title"]
