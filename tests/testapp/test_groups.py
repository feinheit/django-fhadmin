from django.contrib import admin
from django.contrib.auth.models import Permission, User
from django.test import Client, RequestFactory, TestCase
from django.test.utils import override_settings

from fhadmin import FHADMIN_GROUPS_REMAINING, Box, Link
from fhadmin.checks import check_settings
from fhadmin.groups import generate_group_list


def summary(groups):
    """``[(title, [(box name, [model or link names])])]``"""
    return [
        (
            str(title),
            [
                (str(box["name"]), [str(model["name"]) for model in box["models"]])
                for box in boxes
            ],
        )
        for title, boxes in groups
    ]


ARTICLES = "Articles"
TESTAPP = ["Articles", "Categories", "Models", "Pages"]


class GroupsTest(TestCase):
    def groups(self, user=None, **kwargs):
        request = RequestFactory().get("/")
        request.user = (
            user
            or User.objects.get_or_create(
                username="admin", defaults={"is_superuser": True}
            )[0]
        )
        return summary(generate_group_list(admin.sites.site, request, **kwargs))

    def check_ids(self):
        return [error.id for error in check_settings(None)]

    def test_default_groups(self):
        self.assertEqual(
            self.groups(),
            [
                ("Modules", [("Testapp", TESTAPP)]),
                (
                    "Preferences",
                    [("Authentication and Authorization", ["Groups", "Users"])],
                ),
            ],
        )
        self.assertEqual(self.check_ids(), [])

    @override_settings(
        FHADMIN_GROUPS={
            "People": ["auth.User"],
            "Content": ["testapp", "*"],
        }
    )
    def test_models_and_remaining(self):
        """Models win over their app, "*" gets the rest"""
        self.assertEqual(
            self.groups(),
            [
                ("People", [("Authentication and Authorization", ["Users"])]),
                (
                    "Content",
                    [
                        ("Testapp", TESTAPP),
                        ("Authentication and Authorization", ["Groups"]),
                    ],
                ),
            ],
        )
        self.assertEqual(self.check_ids(), [])

    @override_settings(FHADMIN_GROUPS={"Content": "testapp"})
    def test_other(self):
        """Without "*" everything else ends up in "Other", and a single
        string is an entry, not a list of characters"""
        self.assertEqual(
            self.groups(),
            [
                ("Content", [("Testapp", TESTAPP)]),
                ("Other", [("Authentication and Authorization", ["Groups", "Users"])]),
            ],
        )

    @override_settings(
        FHADMIN_GROUPS={
            "People": [("auth.User", "auth.Group", "testapp.Category")],
            "Content": [Box("Writing", ["testapp.Article", "testapp.Page"]), "*"],
        }
    )
    def test_boxes(self):
        self.assertEqual(
            self.groups(),
            [
                (
                    "People",
                    [
                        (
                            "Authentication and Authorization",
                            ["Categories", "Groups", "Users"],
                        )
                    ],
                ),
                (
                    "Content",
                    [("Writing", ["Articles", "Pages"]), ("Testapp", ["Models"])],
                ),
            ],
        )
        self.assertEqual(self.check_ids(), [])

    @override_settings(
        FHADMIN_GROUPS={
            "Content": [
                Box(
                    "Tools",
                    [
                        Link("Report", "/admin/report/"),
                        "testapp.Article",
                        Link("Index", "admin:index", permission="auth.view_user"),
                        Link("Hidden", "/hidden/", permission=lambda request: False),
                    ],
                ),
                Link("Standalone", "/admin/standalone/"),
            ],
            "Rest": ["*"],
        }
    )
    def test_links(self):
        self.assertEqual(
            self.groups()[0],
            (
                "Content",
                [
                    ("Tools", ["Articles", "Report", "Index"]),
                    ("Standalone", ["Standalone"]),
                ],
            ),
        )

        request = RequestFactory().get("/")
        request.user = User.objects.get(username="admin")
        [_title, boxes] = next(generate_group_list(admin.sites.site, request))
        self.assertEqual(
            [model["admin_url"] for model in boxes[0]["models"][1:]],
            ["/admin/report/", "/admin/"],
        )
        self.assertEqual(boxes[1]["app_url"], "/admin/standalone/")
        self.assertEqual(self.check_ids(), [])

    @override_settings(
        FHADMIN_GROUPS={
            "Tools": [
                Box(
                    "Tools", [Link("Index", "admin:index", permission="auth.view_user")]
                )
            ]
        }
    )
    def test_link_permission(self):
        user = User.objects.create(username="staff", is_staff=True)
        user.user_permissions.add(Permission.objects.get(codename="view_group"))
        self.assertEqual(
            self.groups(user),
            [("Other", [("Authentication and Authorization", ["Groups"])])],
        )

        user.user_permissions.add(Permission.objects.get(codename="view_user"))
        user = User.objects.get(pk=user.pk)  # Reset the permission cache
        self.assertEqual(self.groups(user)[0], ("Tools", [("Tools", ["Index"])]))

    def test_filter_by_app_label(self):
        self.assertEqual(
            self.groups(only_app_label="testapp"), [("Modules", [("Testapp", TESTAPP)])]
        )

    @override_settings(
        FHADMIN_GROUPS=[
            ("Content", ("testapp",)),
            ("Rest", (FHADMIN_GROUPS_REMAINING,)),
        ]
    )
    def test_deprecated_list(self):
        self.assertEqual(
            self.groups(),
            [
                ("Content", [("Testapp", TESTAPP)]),
                ("Rest", [("Authentication and Authorization", ["Groups", "Users"])]),
            ],
        )
        self.assertEqual(self.check_ids(), ["fhadmin.W002"])

    @override_settings(FHADMIN_GROUPS=[("Content", ("testapp", "REMAINING"))])
    def test_deprecated_remaining_value(self):
        """The value of FHADMIN_GROUPS_REMAINING before it became "*" """
        self.assertEqual(self.groups()[0][1][1][0], "Authentication and Authorization")

    @override_settings(
        FHADMIN_GROUPS={
            "Content": ["testapp", "does_not_exist", "testapp.DoesNotExist", 42],
            "Boxes": [("auth", "*"), ("auth", 42)],
        }
    )
    def test_checks(self):
        self.assertEqual(
            self.check_ids(),
            [
                "fhadmin.W001",
                "fhadmin.W001",
                "fhadmin.E001",
                "fhadmin.E002",
                "fhadmin.E001",
            ],
        )
        # Unknown entries are ignored when rendering
        self.assertEqual(self.groups()[0], ("Content", [("Testapp", TESTAPP)]))

    @override_settings(FHADMIN_MERGE={"testapp": "auth"})
    def test_merge_apps(self):
        self.assertEqual(
            self.groups(),
            [
                (
                    "Preferences",
                    [
                        (
                            "Authentication and Authorization",
                            [
                                "Articles",
                                "Categories",
                                "Groups",
                                "Models",
                                "Pages",
                                "Users",
                            ],
                        )
                    ],
                )
            ],
        )
        self.assertEqual(self.check_ids(), ["fhadmin.W003"])

    @override_settings(FHADMIN_MERGE={"does_not_exist": "auth"})
    def test_merge_apps_invalid_source(self):
        self.assertEqual(len(self.groups()), 2)

    @override_settings(FHADMIN_MERGE={"testapp": "does_not_exist"})
    def test_merge_apps_invalid_target(self):
        self.assertEqual(len(self.groups()), 2)


class DashboardTest(TestCase):
    @override_settings(
        FHADMIN_GROUPS={
            "Content": [Box("Tools", [Link("Report", "/admin/report/")]), "*"],
        }
    )
    def test_link_on_dashboard(self):
        client = Client()
        client.force_login(
            User.objects.create(username="test", is_staff=True, is_superuser=True)
        )
        response = client.get("/admin/")
        self.assertContains(response, '<a href="/admin/report/">Report</a>', html=False)
        self.assertContains(response, "<h2>Content</h2>")
