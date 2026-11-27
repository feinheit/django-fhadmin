from django.apps import AppConfig
from django.core import checks


class FHAdminConfig(AppConfig):
    name = "fhadmin"

    def ready(self):
        from django.contrib import admin

        from fhadmin.checks import check_settings

        admin.site.enable_nav_sidebar = False
        checks.register(check_settings)
