import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _

from star.models import Star


class Planet(models.Model):
    DETECTION_METHODS = (
        (1, _('Radial Velocity')),
        (2, _('Pulsar')),
        (3, _('Microlensing')),
        (4, _('Imaging')),
        (5, _('Primary Transit')),
        (6, _('Astrometry')),
        (7, _('TTV')),
        (8, _('Other')),
        (9, _('Secondary Transit')),
    )

    uuid = models.UUIDField(_('UUID'), default=uuid.uuid4, db_index=True)

    host = None

    name = models.CharField(_('Name'), max_length=120, blank=False, null=False)
    detection_method = models.PositiveSmallIntegerField(_('Status'), choices=DETECTION_METHODS, blank=False, null=False,
                                                        default=1)

    # mass
    mass = models.DecimalField(_('Mass'), max_digits=6, decimal_places=2, null=True, blank=True)
    mass_error_min = models.DecimalField(_('Mass error margin (min)'), max_digits=6, decimal_places=2,
                                         null=True, blank=True)
    mass_error_max = models.DecimalField(_('Mass error margin (max)'), max_digits=6, decimal_places=2,
                                         null=True, blank=True)



    def __str__(self):
        return self.name