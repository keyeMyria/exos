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

    def fetch_data(self):
        params = settings.DATA_SOURCE_PARAMS
        params['table'] = DATA_SOURCE_TABLE_NAME
        # print(params)
        url = '%s?%s' % (settings.DATA_SOURCE_URL, urlparse.urlencode(params))
        df = pd.read_csv(url)
        # print(df.head())
        for index, row in df.iterrows():
            try:
                self.get(
                    name=row.star_name
                )
            except Star.DoesNotExist:
                pass
                star = Star(
                    name=row.star_name,
                    name_hip=row.hip_name if pd.notna(row.hip_name) else None,
                    name_hd=row.hd_name if pd.notna(row.hd_name) else None,
                    name_gj=row.gj_name if pd.notna(row.gj_name) else None,
                    name_tm=row.tm_name if pd.notna(row.tm_name) else None,
                    is_exocat=True if row.st_exocatflag == 1 else False,
                    is_coronag=True if row.st_coronagflag == 1 else False,
                    is_starshade=True if row.st_starshadeflag == 1 else False,
                    is_wfirst=True if row.st_wfirstflag == 1 else False,
                    is_lbti=True if row.st_lbtiflag == 1 else False,
                    is_rv=True if row.st_rvflag == 1 else False,
                    nb_planets=row.st_ppnum if pd.notna(row.st_ppnum) else 0,
                    ra=row.rastr if pd.notna(row.rastr) else None,
                    dec=row.decstr if pd.notna(row.decstr) else None,
                    distance=row.st_dist if pd.notna(row.st_dist) else None,
                    distance_err_max=row.st_disterr1 if pd.notna(row.st_disterr1) else None,
                    distance_err_min=row.st_disterr2 if pd.notna(row.st_disterr2) else None,
                    vmag=row.st_vmag if pd.notna(row.st_vmag) else None,
                    vmag_err=row.st_vmagerr if pd.notna(row.st_vmagerr) else None,
                    bmv=row.st_bmv if pd.notna(row.st_bmv) else None,
                    bmv_err=row.st_bmverr if pd.notna(row.st_bmverr) else None,
                    stellar_type=row.st_spttype if pd.notna(row.st_spttype) else None,
                    luminosity_bolo=row.st_lbol if pd.notna(row.st_lbol) else None,
                    luminosity_bolo_err=row.st_lbolerr if pd.notna(row.st_lbolerr) else None,
                )
                # print(star.__dict__)
                star.save()


class Star(models.Model):
    """
    Model for stars
    native fields are taken "as is" from the data source but renamed
    """

    uuid = models.UUIDField(_('UUID'), default=uuid.uuid4, db_index=True)

    # native fields
    name = models.CharField(_('Name'), max_length=120, blank=False, null=False, default=None,
                                 help_text=_('[star_name] Stellar name most commonly used'))
    name_hip = models.CharField(_('HIP Name'), max_length=120, blank=True, null=True,
                                help_text=_('[hip_name] Name of the star as given by the Hipparcos Catalog'))
    name_hd = models.CharField(_('HD Name'), max_length=120, blank=True, null=True,
                               help_text=_('[hd_name] Name of the star as given by the Henry Draper Catalog'))
    name_gj = models.CharField(_('GJ Name'), max_length=120, blank=True, null=True,
                               help_text=_('[gj_name] Name of the star as given by the Gliese Jahreiss Catalog'))
    name_tm = models.CharField(_('TM Name'), max_length=120, blank=True, null=True,
                               help_text=_('[tm_name] 2MASS designation'))
    is_exocat = models.BooleanField(_('ExoCat List'), max_length=120, blank=False, default=False,
                                        help_text=_('[st_exocatflag] Flag indicating if a star is on the ExoCat '
                                                    'Directing Imaging Mission star list'))
    is_coronag = models.BooleanField(_('Exo-C Probe List'), max_length=120, blank=False, default=False,
                                        help_text=_('[st_coronagflag] Flag indicating if a star is on the Exo-C '
                                                    'Coronagraph Probe star list'))
    is_starshade = models.BooleanField(_('Exo-S Probe List'), max_length=120, blank=False, default=False,
                                        help_text=_('[st_starshadeflag] Flag indicating if a star is on the Exo-S '
                                                    'Starshade Probe star list'))
    is_wfirst = models.BooleanField(_('WFIRST List'), max_length=120, blank=False, default=False,
                                        help_text=_('[st_wfirstflag] Flag indicating is a star is on the WFIRST '
                                                    'coronagraph exoplanet list'))
    is_lbti = models.BooleanField(_('LBTI List'), max_length=120, blank=False, default=False,
                                        help_text=_('[st_lbtiflag] Flag indicating if a star is on the LBTI s'
                                                    'urvey list'))
    is_rv = models.BooleanField(_('Known RV Data'), max_length=120, blank=False, default=False,
                                        help_text=_('[st_rvflag] Flag indicating if a star has RV data, either a '
                                                    'detection or a non-detection'))
    nb_planets = models.PositiveSmallIntegerField(_('Nb planets'), blank=False, null=False, default=0,
                                                help_text=_('[st_ppnum] Number of planets'))
    ra = models.CharField(_('Right ascension'), blank=True, null=True, max_length=48,
                                                help_text=_('[rastr] Right Ascension in sexagesimal format.'))
    dec = models.CharField(_('Declination'), blank=True, null=True, max_length=48,
                                                help_text=_('[decstr] Declination in sexagesimal notation'))
    distance = models.DecimalField(_('Distance'), max_digits=6, decimal_places=2, null=True, blank=True,
                                   help_text=_('[st_dist] Distance to the planetary system in units of parsecs'))
    distance_err_max = models.DecimalField(_('Distance maximum margin for error'), max_digits=6, decimal_places=2,
                                           null=True, blank=True,
                                           help_text=_('[st_disterr1] in parsecs'))
    distance_err_min = models.DecimalField(_('Distance minimum margin for error'), max_digits=6, decimal_places=2,
                                           null=True, blank=True,
                                           help_text=_('[st_disterr2] in parsecs'))
    vmag = models.DecimalField(_('V-Band'), max_digits=6, decimal_places=2,
                               null=True, blank=True,
                               help_text=_('[st_vmag] Brightness as measured using the V band in units of magnitudes'))
    vmag_err = models.DecimalField(_('V-Band margin for error'), max_digits=6, decimal_places=2,
                               null=True, blank=True,
                               help_text=_('[st_vmagerr]'))
    bmv = models.DecimalField(_('B-V'), max_digits=6, decimal_places=2,
                               null=True, blank=True,
                               help_text=_('[st_bmv] Color of the star as measured by the difference '
                                           'between B and V bands'))
    bmv_err = models.DecimalField(_('B-V margin for error'), max_digits=6, decimal_places=2,
                              null=True, blank=True,
                              help_text=_('[st_bmverr]'))
    stellar_type = models.CharField(_('Stellar Spectral Type '), max_length=12, blank=True, null=True,
                                 help_text=_('[st_spttype] SClassification of the star based on their spectral '
                                             'characteristics following the Morgan-Keenan system'))
    luminosity_bolo = models.DecimalField(_('Stellar Bolometric Luminosity'), max_digits=6, decimal_places=2,
                              null=True, blank=True,
                              help_text=_('[st_lbol] (log(solar)) Amount of energy emitted by a star per unit time, '
                                          'measured in units of solar luminosities. The bolometric corrections are '
                                          'derived from V-K or B-V colors'))
    luminosity_bolo_err = models.DecimalField(_('Stellar Bolometric Luminosity margin for error'), max_digits=6,
                                              decimal_places=2, null=True, blank=True, help_text=_('[st_lbolerr]'))


    objects = StarManager()


    def __str__(self):
        return self.name

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

        return x,y,z