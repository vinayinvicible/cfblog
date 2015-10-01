import datetime

from django.db import models


class CmsBlogPostManager(models.Manager):

    def published(self):
        return self.get_queryset().filter(status__gte=2, publish__lte=datetime.datetime.now())


class CmsBlogCategoryManager(models.Manager):

    def active(self):
        return self.get_queryset().filter(is_active=True)

    def top(self):
        return self.get_queryset().filter(is_active=True, level=1)
