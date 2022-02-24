from django.db import models


class Model(models.Model):
    title = models.CharField(max_length=100)
