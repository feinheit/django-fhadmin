from django.contrib.auth.models import User
from django.test import Client, TestCase


class AdminTest(TestCase):
    def login(self):
        client = Client()
        u = User.objects.create(
            username="test", is_active=True, is_staff=True, is_superuser=True
        )
        client.force_login(u)
        return client

    def test_dashboard_superuser(self):
        client = self.login()
        response = client.get("/admin/")
        self.assertContains(response, '<div class="groups">')
        self.assertContains(response, "<h2>Modules</h2>")
        self.assertContains(response, "<h2>Preferences</h2>")
        # print(response, response.content.decode("utf-8"))

    def test_dashboard_no_rights(self):
        client = Client()
        u = User.objects.create(
            username="test", is_active=True, is_staff=True, is_superuser=False
        )
        client.force_login(u)
        response = client.get("/admin/")
        # print(response, response.content.decode("utf-8"))
        self.assertContains(
            response, "<p>You don’t have permission to view or edit anything.</p>"
        )
        self.assertNotContains(response, '<div class="groups">')
