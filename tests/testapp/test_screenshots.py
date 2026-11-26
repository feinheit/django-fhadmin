"""
Screenshots of the themed admin in light and dark mode.

The screenshots are written to ``tests/screenshots/django-<version>/`` and
aren't compared automatically; look at them when changing the theme.
"""

import datetime
from pathlib import Path

import django
import pytest
from django.contrib.auth.models import User

from testapp.models import (
    Article,
    ArticleLink,
    ArticleNote,
    Category,
    Container,
    Page,
    RichText,
)


pytestmark = pytest.mark.django_db(transaction=True)

SCREENSHOTS = (
    Path(__file__).parent.parent
    / "screenshots"
    / "django-{}.{}".format(*django.VERSION[:2])
)
SCHEMES = ["light", "dark"]


@pytest.fixture
def data():
    User.objects.create_superuser("admin", "admin@example.com", "password")
    news = Category.objects.create(name="News")
    Category.objects.create(name="Events")
    for i in range(12):
        Article.objects.create(
            title=f"Article number {i + 1}",
            slug=f"article-{i + 1}",
            category=news,
            status=["draft", "review", "published"][i % 3],
            is_featured=i % 4 == 0,
            published_on=datetime.date(2026, 1 + i % 12, 1 + i),
        )
    article = Article.objects.first()
    article.lead = "<p>A <strong>short</strong> lead for the first article.</p>"
    article.save()
    ArticleLink.objects.create(
        article=article, title="Django", url="https://www.djangoproject.com/"
    )
    ArticleNote.objects.create(article=article, author="Editor", note="Looks good.")

    page = Page.objects.create(title="Large page")
    ordering = iter(range(10, 1000, 10))

    def text(depth=0, region="main"):
        return RichText.objects.create(
            parent=page,
            region=region,
            ordering=next(ordering),
            depth=depth,
            text="<h2>Heading</h2><p>A paragraph with some text.</p>",
        )

    def container(title, depth=0, region="main"):
        return Container.objects.create(
            parent=page,
            region=region,
            ordering=next(ordering),
            depth=depth,
            title=title,
        )

    text()
    container("Accordion")
    container("Item: Opening hours", depth=1)
    text(depth=2)
    text(depth=2)
    container("Item: Prices", depth=1)
    container("Columns", depth=2)
    text(depth=3)
    text(depth=3)
    text()
    text(region="sidebar")
    return {"article": article, "page": page}


def login(page, live_server):
    page.goto(f"{live_server.url}/admin/login/")
    page.fill("#id_username", "admin")
    page.fill("#id_password", "password")
    page.click("input[type=submit]")
    page.wait_for_url(f"{live_server.url}/admin/")


def shoot(page, name, scheme):
    SCREENSHOTS.mkdir(parents=True, exist_ok=True)
    # Let transitions finish and make the viewport as tall as the document so
    # that sticky elements end up where they belong.
    page.set_viewport_size({"width": 1280, "height": 800})
    page.wait_for_timeout(300)
    height = page.evaluate("document.documentElement.scrollHeight")
    page.set_viewport_size({"width": 1280, "height": max(800, height)})
    page.screenshot(path=SCREENSHOTS / f"{name}-{scheme}.png", full_page=True)


@pytest.mark.parametrize("scheme", SCHEMES)
def test_login(page, live_server, data, scheme):
    page.emulate_media(color_scheme=scheme)
    page.goto(f"{live_server.url}/admin/login/")
    shoot(page, "login", scheme)
    page.fill("#id_username", "admin")
    page.fill("#id_password", "wrong")
    page.click("input[type=submit]")
    shoot(page, "login-error", scheme)


@pytest.mark.parametrize("scheme", SCHEMES)
def test_admin(page, live_server, data, scheme):
    page.emulate_media(color_scheme=scheme)
    login(page, live_server)
    url = live_server.url

    shoot(page, "index", scheme)
    page.click("#site-name")
    shoot(page, "quickpanel", scheme)

    page.goto(f"{url}/admin/testapp/article/?status__exact=draft")
    page.goto(f"{url}/admin/testapp/article/")
    page.locator(".action-select").nth(1).check()
    page.locator(".action-select").nth(2).check()
    page.select_option("select[name=action]", "make_published")
    shoot(page, "changelist", scheme)
    page.click("button[name=index]")
    shoot(page, "changelist-message", scheme)

    article = data["article"]
    page.goto(f"{url}/admin/testapp/article/{article.pk}/change/")
    page.wait_for_selector(".prose-editor")
    page.focus("#id_title")
    shoot(page, "changeform", scheme)

    page.fill("#id_title", "")
    page.click("input[name=_save]")
    shoot(page, "changeform-errors", scheme)

    page.goto(f"{url}/admin/testapp/article/{article.pk}/delete/")
    shoot(page, "delete", scheme)

    page.goto(f"{url}/admin/password_change/")
    shoot(page, "password-change", scheme)

    page.goto(f"{url}/admin/testapp/page/{data['page'].pk}/change/")
    page.wait_for_selector(".order-machine")
    shoot(page, "content-editor", scheme)

    # Django's own theme toggle sets html[data-theme]
    page.goto(f"{url}/admin/testapp/article/{article.pk}/change/")
    page.evaluate(
        "scheme => { document.documentElement.dataset.theme = scheme === 'light' ? 'dark' : 'light' }",
        scheme,
    )
    shoot(page, "changeform-toggled", scheme)


@pytest.mark.parametrize("scheme", SCHEMES)
@pytest.mark.parametrize("theme", ["auto", "light", "dark"])
def test_brand_colours(page, live_server, data, scheme, theme):
    # Django's base.css sets its own blue under html[data-theme="light"]
    page.emulate_media(color_scheme=scheme)
    login(page, live_server)
    page.evaluate(f"document.documentElement.dataset.theme = {theme!r}")
    page.wait_for_timeout(300)
    header = page.eval_on_selector(
        "#header", "el => getComputedStyle(el).backgroundColor"
    )
    assert header == "rgb(12, 75, 51)"


ENVIRONMENT_STYLE = """
const style = document.createElement("style")
style.textContent = `SELECTOR {
  --primary: #aa0000; --secondary: #810000; --accent: yellow;
}`
document.head.append(style)
"""


@pytest.mark.parametrize("scheme", SCHEMES)
@pytest.mark.parametrize(
    "theme,selector",
    [
        # The snippet from 406.ch works when the theme is "auto" (the default)
        ("auto", ":root"),
        # The documented selector also works when a theme has been chosen
        ("light", "html[data-theme], :root"),
        ("dark", "html[data-theme], :root"),
    ],
)
def test_environment_colours(page, live_server, data, scheme, theme, selector):
    page.emulate_media(color_scheme=scheme)
    login(page, live_server)
    page.goto(f"{live_server.url}/admin/testapp/article/add/")
    page.evaluate(f"document.documentElement.dataset.theme = {theme!r}")
    page.evaluate(ENVIRONMENT_STYLE.replace("SELECTOR", selector))
    page.wait_for_timeout(300)  # Buttons transition their background

    def css(selector, prop):
        return page.eval_on_selector(selector, f"el => getComputedStyle(el).{prop}")

    assert css("#header", "backgroundColor") == "rgb(129, 0, 0)"
    assert css("#site-name", "color") == "rgb(255, 255, 0)"
    assert css("input[name=_save]", "backgroundColor") == "rgb(129, 0, 0)"
    if theme == "auto" and scheme == "light":
        shoot(page, "environment", scheme)
