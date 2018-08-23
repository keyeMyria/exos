import uuid
import pandas as pd
import urllib.parse as urlparse
import math
import re

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


DATA_SOURCE_TABLE_NAME = 'missionstars'

RA_RE = re.compile('(\d{2})h(\d{2})m(\d{2}\.\d{2})s')
DEC_RE = re.compile('(\+|-)(\d{2})d(\d{2})m(\d{2}\.\d{1})s')


class StarManager(models.Manager):

    pass

    # def fetch_data(self):
    #     params = settings.DATA_SOURCE_PARAMS
    #     params['table'] = DATA_SOURCE_TABLE_NAME
    #     # print(params)
    #     url = '%s?%s' % (settings.DATA_SOURCE_URL, urlparse.urlencode(params))
    #     df = pd.read_csv(url)
    #     # print(df.head())
    #     for index, row in df.iterrows():
    #         try:
    #             self.get(
    #                 name=row.star_name
    #             )
    #         except Star.DoesNotExist:
    #             pass
    #             star = Star(
    #                 name=row.star_name,
    #                 name_hip=row.hip_name if pd.notna(row.hip_name) else None,
    #                 name_hd=row.hd_name if pd.notna(row.hd_name) else None,
    #                 name_gj=row.gj_name if pd.notna(row.gj_name) else None,
    #                 name_tm=row.tm_name if pd.notna(row.tm_name) else None,
    #                 is_exocat=True if row.st_exocatflag == 1 else False,
    #                 is_coronag=True if row.st_coronagflag == 1 else False,
    #                 is_starshade=True if row.st_starshadeflag == 1 else False,
    #                 is_wfirst=True if row.st_wfirstflag == 1 else False,
    #                 is_lbti=True if row.st_lbtiflag == 1 else False,
    #                 is_rv=True if row.st_rvflag == 1 else False,
    #                 nb_planets=row.st_ppnum if pd.notna(row.st_ppnum) else 0,
    #                 ra=row.rastr if pd.notna(row.rastr) else None,
    #                 dec=row.decstr if pd.notna(row.decstr) else None,
    #                 distance=row.st_dist if pd.notna(row.st_dist) else None,
    #                 distance_err_max=row.st_disterr1 if pd.notna(row.st_disterr1) else None,
    #                 distance_err_min=row.st_disterr2 if pd.notna(row.st_disterr2) else None,
    #                 vmag=row.st_vmag if pd.notna(row.st_vmag) else None,
    #                 vmag_err=row.st_vmagerr if pd.notna(row.st_vmagerr) else None,
    #                 bmv=row.st_bmv if pd.notna(row.st_bmv) else None,
    #                 bmv_err=row.st_bmverr if pd.notna(row.st_bmverr) else None,
    #                 stellar_type=row.st_spttype if pd.notna(row.st_spttype) else None,
    #                 luminosity_bolo=row.st_lbol if pd.notna(row.st_lbol) else None,
    #                 luminosity_bolo_err=row.st_lbolerr if pd.notna(row.st_lbolerr) else None,
    #             )
    #             # print(star.__dict__)
    #             star.save()


class Star(models.Model):
    """
    Model for stars
    """

    OPTICAL_MAGNITUDE_BAND = (
        (1, _('V (Johnson)')),
        (2, _('Kepler-band')),
    )

    uuid = models.UUIDField(_('UUID'), default=uuid.uuid4, db_index=True)

    # native fields
    name = models.CharField(_('Name'), max_length=120, blank=False, null=False, default=None,
                                 help_text=_('[pl_hostname] Stellar name most commonly used'))

    # right ascension
    ra_str = models.CharField(_('Right ascension'), blank=True, null=True, max_length=20,
        help_text=_('[ra_str] Right Ascension in sexagesimal format.'))
    ra_str_err = models.DecimalField(_('Right ascension error margin'), blank=True, null=True,
        max_digits=20, decimal_places=10, help_text=_('[st_raerr]'))
    ra = models.DecimalField(_('Right ascension'), max_digits=20, decimal_places=10,
        null=True, blank=True, help_text=_('[ra] in decimal degrees'))

    # declination
    dec_str = models.CharField(_('Declination'), blank=True, null=True, max_length=20,
        help_text=_('[dec_str] Declination in sexagesimal format.'))
    dec_str_err = models.DecimalField(_('Declination error margin'), blank=True, null=True,
        max_digits=20, decimal_places=10, help_text=_('[st_decerr]'))
    dec = models.DecimalField(_('Declination'), max_digits=20, decimal_places=10,
        null=True, blank=True, help_text=_('[dec] in decimal degrees'))

    # distance
    distance = models.DecimalField(_('Distance'), max_digits=20, decimal_places=10, null=True, blank=True,
        help_text=_('[st_dist] Distance to the planetary system in units of parsecs'))
    distance_err_up = models.DecimalField(_('Distance upper error margin'), max_digits=20, decimal_places=10,
        null=True, blank=True, help_text=_('[st_disterr1] in parsecs'))
    distance_err_low = models.DecimalField(_('Distance lower error margin'), max_digits=20, decimal_places=10,
        null=True, blank=True, help_text=_('[st_disterr2] in parsecs'))
    distance_limit = models.DecimalField(_('Distance limit'), max_digits=20, decimal_places=10, null=True, blank=True,
        help_text=_('[st_distlim]'))
    distance_nb_measures = models.PositiveSmallIntegerField(_('Distance number of measures'), blank=False,
        null=False, default=0, help_text=_('[st_distn]'))

    # optical magnitude
    magnitude_optical = models.DecimalField(_('Optical magnitude (mag)'), max_digits=20, decimal_places=10, null=True, blank=True,
        help_text=_('[st_optmag] Brightness of the host star as measured using the V (Johnson) or the Kepler-band '
                    'in units of magnitudes'))
    magnitude_optical_err = models.DecimalField(_('Optical magnitude error margin'), max_digits=20, decimal_places=10,
        null=True, blank=True, help_text=_('[st_optmagerr]'))
    magnitude_optical_limit = models.DecimalField(_('Optical magnitude limit'), max_digits=20, decimal_places=10,
        null=True, blank=True, help_text=_('[st_optmaglim]'))
    magnitude_optical_band = models.PositiveSmallIntegerField(_('Optical magnitude band'), choices=OPTICAL_MAGNITUDE_BAND,
        blank=False, null=False, default=1, help_text=_('[st_optband]'))

    # gaia magnitude
    magnitude_gaia =  models.DecimalField(_('G-band (Gaia) (mag)'), max_digits=20, decimal_places=10, null=True, blank=True,
        help_text=_('[gaia_gmag] Brightness of the host star as measuring using the Gaia band in units of magnitudes'))
    magnitude_gaia_err = models.DecimalField(_('G-band (Gaia) error margin'), max_digits=20, decimal_places=10,
        null=True, blank=True, help_text=_('[gaia_gmagerr]'))
    magnitude_gaia_limit = models.DecimalField(_('G-band (Gaia) limit'), max_digits=20, decimal_places=10,
        null=True, blank=True, help_text=_('[gaia_gmaglim]'))

    # temperature
    temperature = models.DecimalField(_('Effective temperature (K)'), max_digits=20, decimal_places=10,
        null=True, blank=True, help_text=_('[st_teff] Temperature of the star as modeled by a black body emitting '
                                           'the same total amount of electromagnetic radiations'))
    temperature_err_up = models.DecimalField(_('Effective temperature upper error margin'), max_digits=20, decimal_places=10,
        null=True, blank=True, help_text=_('[st_tefferr1] in parsecs'))
    temperature_err_low = models.DecimalField(_('Effective temperature lower error margin'), max_digits=20, decimal_places=10,
        null=True, blank=True, help_text=_('[st_tefferr2] in parsecs'))
    temperature_limit = models.DecimalField(_('Effective temperature limit'), max_digits=20, decimal_places=10, null=True,
        blank=True, help_text=_('[st_tefflim]'))
    temperature_nb_measures = models.PositiveSmallIntegerField(_('Effective temperature number of measures'), blank=False,
        null=False, default=0, help_text=_('[st_teffn]'))

    # mass
    mass = models.DecimalField(_('Mass (solar mass)'), max_digits=20, decimal_places=10,
        null=True, blank=True, help_text=_('[st_mass] Amount of matter contained in the star, measured '
                                           'in units of masses of the Sun'))
    mass_err_up = models.DecimalField(_('Mass upper error margin'), max_digits=20, decimal_places=10,
        null=True, blank=True, help_text=_('[st_masserr1] in parsecs'))
    mass_err_low = models.DecimalField(_('Mass lower error margin'), max_digits=20, decimal_places=10,
        null=True, blank=True, help_text=_('[st_masserr2] in parsecs'))
    mass_limit = models.DecimalField(_('Mass limit'), max_digits=20, decimal_places=10, null=True, blank=True,
        help_text=_('[st_masslim]'))
    mass_nb_measures = models.PositiveSmallIntegerField(_('Mass number of measures'), blank=False,
        null=False, default=0, help_text=_('[st_massn]'))

    # radius
    radius = models.DecimalField(_('Radius (solar radii)'), max_digits=20, decimal_places=10,
         null=True, blank=True, help_text=_('[pl_radj] Amount of matter contained in the star, measured '
                                           'in units of masses of the Sun'))
    radius_err_up = models.DecimalField(_('Radius upper error margin'), max_digits=20, decimal_places=10,
         null=True, blank=True, help_text=_('[pl_radjerr1] in parsecs'))
    radius_err_low = models.DecimalField(_('Radius lower error margin'), max_digits=20, decimal_places=10,
         null=True, blank=True, help_text=_('[pl_radjerr2] in parsecs'))
    radius_limit = models.DecimalField(_('Radius limit'), max_digits=20, decimal_places=10, null=True, blank=True,
         help_text=_('[pl_radjlim]'))
    radius_nb_measures = models.PositiveSmallIntegerField(_('Radius number of measures'), blank=False,
         null=False, default=0, help_text=_('[pl_radn]'))

    objects = StarManager()


    def __str__(self):
        return self.name

    @property
    def nb_planets(self):
        from planet.models import Planet
        return Planet.objects.filter(
            star=self
        ).count()

    @property
    def cartesian_coordinates(self):
        """
        Returns the cartesian coordinates based RA, DEC and distance (pc)
        sources:
        http://fmwriters.com/Visionback/Issue14/wbputtingstars.htm
        https://math.stackexchange.com/questions/15323/how-do-i-calculate-the-cartesian-coordinates-of-stars
        """
        # extract RA items
        ra_hours, ra_minutes, ra_seconds = RA_RE.match(str(self.ra)).groups()
        # then cast
        ra_hours = int(ra_hours)
        ra_minutes = int(ra_minutes)
        ra_seconds = float(ra_seconds)

        # extract DEC items
        dec_sign, dec_degrees, dec_minutes, dec_seconds = DEC_RE.match(str(self.dec)).groups()
        # then cast
        dec_sign = -1 if dec_sign == '-' else 1
        dec_degrees = int(dec_degrees)
        dec_minutes = int(dec_minutes)
        dec_seconds = float(dec_seconds)

        # to degrees
        a = (ra_hours*15) + (ra_minutes*0.25) + (ra_seconds*0.004166)
        b = abs(dec_degrees + dec_minutes/60 + dec_seconds/3600) * dec_sign

        #  to radians
        a = math.radians(a)
        b = math.radians(b)

        distance = float(self.distance)

        x = (distance * math.cos(b)) * math.cos(a)
        y = (distance * math.cos(b)) * math.sin(a)
        z = distance * math.sin(b)

        return x, y, z