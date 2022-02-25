from django.apps import AppConfig


class FHAdminConfig(AppConfig):
    name = "fhadmin"

    def ready(self):
        from django.contrib import admin

        admin.site.enable_nav_sidebar = False
