import os


# Playwright runs an event loop; the live server and ORM calls in the tests
# are synchronous.
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
