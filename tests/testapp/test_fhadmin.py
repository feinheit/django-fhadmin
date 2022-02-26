from unittest import skipIf

from django import VERSION
from django.contrib import admin
from django.contrib.auth.models import User
from django.test import Client, RequestFactory, TestCase
from django.test.utils import override_settings

from fhadmin.templatetags.fhadmin_groups import generate_group_list


class AdminTest(TestCase):
    def login(self):
        client = Client()
        u = User.objects.create(
            username="test", is_active=True, is_staff=True, is_superuser=True
        )
        client.force_login(u)
        return client

    def test_dashboard(self):
        client = self.login()
        response = client.get("/admin/")
        self.assertContains(response, '<div class="groups">')
        self.assertContains(response, "<h2>Modules</h2>")
        self.assertContains(response, "<h2>Preferences</h2>")

        # print(response, response.content.decode("utf-8"))

    def generate_superuser_group_list(self, **kwargs):
        request = RequestFactory().get("/")
        request.user = User.objects.create(is_superuser=True)
        return list(generate_group_list(admin.sites.site, request, **kwargs))

    def test_default_groups(self):
        groups = self.generate_superuser_group_list()
        self.assertEqual(len(groups), 2)
        self.assertEqual(groups[0][0], "Modules")
        self.assertEqual(groups[0][1][0]["app_label"], "testapp")
        self.assertEqual(len(groups[0][1][0]["models"]), 1)

    def test_filter_by_app_label(self):
        groups = self.generate_superuser_group_list(only_app_label="testapp")
        self.assertEqual(len(groups), 1)

    @skipIf(VERSION < (4, 0), "Django < 4.0 does not include the model in the app list")
    @override_settings(FHADMIN_MERGE={"testapp": "auth"})
    def test_merge_apps(self):
        groups = self.generate_superuser_group_list()
        self.assertEqual(len(groups), 1)
        self.assertEqual(groups[0][0], "Preferences")
        self.assertEqual(groups[0][1][0]["app_label"], "auth")
        self.assertEqual(
            [model["model"]._meta.label_lower for model in groups[0][1][0]["models"]],
            ["auth.group", "testapp.model", "auth.user"],
        )

    @override_settings(FHADMIN_MERGE={"does_not_exist": "auth"})
    def test_merge_apps_invalid_source(self):
        groups = self.generate_superuser_group_list()
        self.assertEqual(len(groups), 2)

    @override_settings(FHADMIN_MERGE={"testapp": "does_not_exist"})
    def test_merge_apps_invalid_target(self):
        groups = self.generate_superuser_group_list()
        self.assertEqual(len(groups), 2)
