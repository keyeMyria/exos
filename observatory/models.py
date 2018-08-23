import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _


class ObservatoryManager(models.Manager):
    pass


class Observatory(models.Model):
    """
    Model for observatories
    Not much data from main data source, so will have to find a way to grab from somewhere else...
    """

    uuid = models.UUIDField(_('UUID'), default=uuid.uuid4, db_index=True)
    name = models.CharField(_('Name'), max_length=255, blank=False, null=False, default=None)

    objects = ObservatoryManager()

    def __str__(self):
        return self.name