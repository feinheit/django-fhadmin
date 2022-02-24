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

    def test_dashboard(self):
        client = self.login()
        response = client.get("/admin/")
        self.assertContains(response, '<div class="groups">')
        self.assertContains(response, "<h2>Modules</h2>")
        self.assertContains(response, "<h2>Preferences</h2>")

        print(response, response.content.decode("utf-8"))
