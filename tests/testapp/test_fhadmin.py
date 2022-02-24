from django.contrib import admin
from django.contrib.auth.models import User
from django.test import Client, RequestFactory, TestCase
from django.test.utils import override_settings

from fhadmin.templatetags.fhadmin_module_groups import generate_group_list


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

    def test_default_groups(self):
        request = RequestFactory().get("/")
        request.user = User.objects.create(is_superuser=True)

        groups = list(generate_group_list(admin.sites.site, request))
        # from pprint import pprint; pprint(groups)

        self.assertEqual(groups[0][0], "Modules")
        self.assertEqual(groups[0][1][0]["app_label"], "testapp")
        self.assertEqual(len(groups[0][1][0]["models"]), 1)

    @override_settings(FHADMIN_MERGE={"testapp": "auth"})
    def test_merge_apps(self):
        request = RequestFactory().get("/")
        request.user = User.objects.create(is_superuser=True)

        groups = list(generate_group_list(admin.sites.site, request))
        # from pprint import pprint; pprint(groups)

        self.assertEqual(groups[0][0], "Preferences")
        self.assertEqual(groups[0][1][0]["app_label"], "auth")
        self.assertEqual(
            {model["model"]._meta.label_lower for model in groups[0][1][0]["models"]},
            {"auth.user", "auth.group", "testapp.model"},
        )
